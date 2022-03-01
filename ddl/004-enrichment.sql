

--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--



do $$
begin
    create domain allowed_enrichment_type as text
    check (
        value in (
            'text',
            'int4',
            'int8',
            'float4',
            'float8',
            'numeric',
            'date',
            'point',
            'date',
            'timestamp',
            'jsonb'
        )
    );
    exception when duplicate_object then null;
end $$;

create or replace function valid_range(type allowed_enrichment_type,is_range boolean,is_multirange boolean) returns boolean as
$$
    return True
$$ language plpython3u;



create table if not exists public_api.enrichment_def (
    id bigint generated by default as identity primary key,
    document_type_id bigint,
    document_metadata_definition_id bigint,
    depends_on_id bigint,
    name text not null unique,
    type allowed_enrichment_type not null,
    id_highwater_mark bigint default 0,
    is_array boolean not null default false,
    is_range boolean not null default false,
    is_multirange boolean not null default false,
    function_name text,
    is_manual boolean not null default false,
    foreign key (depends_on_id) references public_api.enrichment_def(id) on update cascade on delete cascade,
    foreign key (document_type_id) references public_api.document_type(id) on update cascade on delete cascade,
    constraint manual_enrichment check (((function_name is null) and (is_manual)) or ((function_name is not null) and (is_manual is false))),
    constraint doc_or_metadata check ((document_metadata_definition_id is not null) or (document_type_id is not null)),
    foreign key (document_metadata_definition_id) references public_api.document_metadata_definition(id) on update cascade on delete cascade

);

comment on table public_api.enrichment_def is 'Defines an enrichment task, that may be auto genreated (e.g. with NLP) or a manual labelling task';

grant select on public_api.enrichment_def to orp_postgrest_web;


create table if not exists enrichment_update (
    id bigint generated by default as identity primary key,
    enrichment_def_id bigint not null,
    rows_processed bigint,
    started_on timestamp not null default now(),
    completed_on timestamp,
    foreign key (enrichment_def_id) references public_api.enrichment_def(id) on update cascade on delete cascade
);


create table if not exists public_api.enrichment (
    id bigint generated by default as identity primary key,
    document_id bigint not null,
    enrichment_def_id bigint not null,
    extent document_extent,
    data text,
    data_type allowed_enrichment_type not null default 'text',
    error jsonb,
    created_on timestamp not null default now(),
    user_id bigint default nullif(current_setting('request.jwt.claim.user_id',true),'')::bigint,
    foreign key (document_id) references public_api.document(id) on update cascade on delete cascade,
    foreign key (enrichment_def_id) references public_api.enrichment_def(id) on update cascade on delete cascade,
    foreign key (user_id) references users(id) on update cascade on delete cascade
);

comment on table public_api.enrichment is 'The unit of encriched data for a particular enrichment_def, there may be many per document';

create index if not exists enrichment_document_id on public_api.enrichment (document_id);
create index if not exists enrichment_document_id on public_api.enrichment (enrichment_def_id);

grant insert,select on public_api.enrichment to orp_postgrest_web;

alter table public_api.enrichment enable row level security;

create policy enrichment_select on public_api.enrichment for select to orp_postgrest_web using (
    true
);

create policy enrichment_insert on public_api.enrichment for insert to orp_postgrest_web with check (
    user_has_role_for_action('manual_enrichment_create') and (select is_manual from public_api.enrichment_def where id = enrichment.enrichment_def_id)
);

create table if not exists public_api.enrichment_feedback (
    id bigint generated by default as identity primary key,
    enrichment_id bigint not null,
    good boolean not null,
    notes text,
    created_on timestamp not null default now(),
    user_id bigint not null default current_setting('request.jwt.claim.user_id',true)::bigint,
    foreign key (enrichment_id) references public_api.enrichment(id) on update cascade on delete cascade,
    foreign key (user_id) references users(id) on update cascade on delete cascade
);

comment on table public_api.enrichment_feedback is 'A piece of feeback from a specific user about a specific enrichment';

create index on public_api.enrichment_feedback(enrichment_id);

grant select,insert on public_api.enrichment_feedback to orp_postgrest_web;

alter table public_api.enrichment_feedback enable row level security;

create policy enrichment_feedback_select on public_api.enrichment_feedback for select to orp_postgrest_web using (
    user_has_role_for_action('enrichment_feedback_read')
);

create policy enrichment_feedback_insert on public_api.enrichment_feedback for insert to orp_postgrest_web with check (
    user_has_role_for_action('enrichment_feedback_create')
);

do $$
begin
    create type feedbackstatus as enum (
        'review_complete',
        'review_incomplete'
    );
    exception when duplicate_object then null;
end $$;

-- create extension btree_gist;

create table if not exists public_api.document_enrichment_feedback_status (
    id bigint generated by default as identity primary key,
    document_id bigint not null,
    feedback_status feedbackstatus not null,
    created_on timestamp not null default now(),
    most_recent boolean not null default true,
    user_id bigint not null default current_setting('request.jwt.claim.user_id',true)::bigint,
    foreign key (document_id) references public_api.document(id) on update cascade on delete cascade,
    foreign key (user_id) references users(id) on update cascade on delete cascade,
    constraint only_one_most_recent exclude using gist(document_id with =,(nullif(most_recent,false)::int) with =)
);

comment on table public_api.document_enrichment_feedback_status is 'Status of the review completeness of an entire document';

create index on public_api.document_enrichment_feedback_status(document_id);

grant select,insert on public_api.document_enrichment_feedback_status to orp_postgrest_web;

alter table public_api.document_enrichment_feedback_status enable row level security;

create policy enrichment_feedback_select on public_api.document_enrichment_feedback_status for select to orp_postgrest_web using (
    user_has_role_for_action('document_enrichment_feedback_status_read')
);

create policy enrichment_feedback_insert on public_api.document_enrichment_feedback_status for insert to orp_postgrest_web with check (
    user_has_role_for_action('document_enrichment_feedback_status_create')
);

create or replace function check_feedback_status() returns trigger as
$$
begin
    if (new.feedback_status::text = 'review_complete') and (
        select bool_or(ef.id is null)
        from public_api.enrichment e
        left join public_api.enrichment_feedback ef on e.id = ef.enrichment_id
        where e.document_id = new.document_id
    ) then
        raise exception 'Not all enrichments for document have had feedback';
    end if;

    return new;
end;
$$ language plpgsql;

create constraint trigger feedback_status_trigger
after insert on public_api.document_enrichment_feedback_status
deferrable initially deferred
for each row
execute procedure check_feedback_status();


create or replace function document_enrichment_feedback_status_before_insert_trigger_f() returns trigger as
$$
begin
    -- set old records
    update public_api.document_enrichment_feedback_status set most_recent = false
    where document_id = new.document_id;

    return new;
end;
$$ language plpgsql security definer;

drop trigger if exists before_insert_trigger on public_api.document_enrichment_feedback_status;
create trigger before_insert_trigger before insert on public_api.document_enrichment_feedback_status
for each row
execute procedure document_enrichment_feedback_status_before_insert_trigger_f();

create or replace function update_enrichment_def(enrichment_def_id bigint, max_rows_per_chunk bigint default 1000, max_total_rows bigint default null) returns void as
$$
declare
q text;
new_max_id bigint;
current_max_id bigint;
last_max_id bigint;
this_chunk_max_id bigint;
last_chunk_max_id bigint;
total_rows bigint := 0;
ed public_api.enrichment_def;
eu_id bigint;
_new_rows bigint;
start_time timestamp;
elapsed numeric;
begin
    -- lock this enrichment_def
    select * into ed from public_api.enrichment_def where id = enrichment_def_id for no key update;

    if ed.is_manual then
        raise notice 'this is a manual enrichment, exiting';
        return;
    end if;


    if ed.document_type_id is not null then
        select coalesce(max(id),0) into new_max_id
        from public_api.document
        where document_type_id = ed.document_type_id;
    else
        select coalesce(max(document_id),0) into new_max_id
        from public_api.document_metadata
        where document_metadata_definition_id = ed.document_metadata_definition_id;
    end if;

    loop
        insert into enrichment_update (enrichment_def_id) values (ed.id) returning id into eu_id;

        select ed.id_highwater_mark into current_max_id;

        raise notice 'id_highwater_mark - % new_max_id - % current_max_id - %',ed.id_highwater_mark,new_max_id,current_max_id;

        select least(new_max_id,(current_max_id + max_rows_per_chunk)) into this_chunk_max_id;

        raise notice 'this_chunk_max_id - %',this_chunk_max_id;

        if this_chunk_max_id = last_chunk_max_id and current_max_id = last_max_id then
            raise notice 'not sure how this happened, but we have gone around the loop twice, exiting';
            exit;
        end if;

        last_chunk_max_id := this_chunk_max_id;
        last_max_id := current_max_id;

        if ed.document_type_id is not null then
            select format($t$
                insert into public_api.enrichment (document_id,enrichment_def_id,data,extent,error)
                select id,%2$s,ef.data,ef.extent,ef.error
                from public_api.document,
                lateral %1$I(raw_text) ef
                where id > %3$s and id <= %4$s
                and document_type_id = %5$s
            $t$,ed.function_name,
                ed.id,
                current_max_id,
                this_chunk_max_id,
                ed.document_type_id
            ) into q;
        else
            select format($t$
                insert into public_api.enrichment (document_id,enrichment_def_id,data,extent,error)
                select document_id,%2$s,ef.data,ef.extent,ef.error
                from public_api.document_metadata,
                lateral %1$I(data) ef
                where document_id > %3$s and document_id <= %4$s
                and document_metadata_definition_id = %5$s
            $t$,ed.function_name,
                ed.id,
                current_max_id,
                this_chunk_max_id,
                ed.document_metadata_definition_id
            ) into q;
        end if;

        raise notice '%',q;
        select clock_timestamp() into start_time;

        execute q;
        get diagnostics _new_rows = ROW_COUNT;
        select extract(epoch from (clock_timestamp() - start_time)) into elapsed;

        raise notice '% rows loaded in % seconds',_new_rows,elapsed;

        select total_rows + _new_rows into total_rows;

        if this_chunk_max_id >= new_max_id then
            raise notice 'reached the end of document type %',ed.document_type_id;
            update enrichment_update set (rows_processed,completed_on) = (total_rows,clock_timestamp()) where id = eu_id;
            update public_api.enrichment_def set id_highwater_mark = this_chunk_max_id where id = enrichment_def_id;
            exit;
        end if;

        if total_rows > max_total_rows then
            raise notice 'reached the max total rows to process';
            exit;
        end if;

        if _new_rows = 0 and total_rows > 0 then
            raise notice 'no more new rows to process';
            exit;
        end if;

    end loop;

end;
$$ language plpgsql;

create or replace function public_api.unenriched_docs(enrichment_def_id bigint) returns setof public_api.document as
$$
    select d.*
    from public_api.document d
    where document_type_id = (select document_type_id from public_api.enrichment_def where id = unenriched_docs.enrichment_def_id)
    and id not in (
        select distinct(document_id)
        from public_api.enrichment
        where enrichment_def_id = unenriched_docs.enrichment_def_id
    );
$$ language sql parallel safe;

comment on function public_api.unenriched_docs is 'document table filter that returns documents for a particular enrichment_def that have zero enrichments created yet (e.g. a manual label)';

grant execute on function public_api.unenriched_docs(bigint) to orp_postgrest_web;


create or replace view public_api.docs_with_outstanding_feedback as
select *
from public_api.document d
where not exists (
    select 1 from public_api.document_enrichment_feedback_status defs
    where defs.document_id = d.id
    and feedback_status = 'review_complete'
    and most_recent = true
) and exists (
    select 1 from public_api.enrichment
    where document_id = d.id
    and data is not null
);



-- Method to determine whether all enrichments have had feedback
-- don't return docs with zero enrichments
-- docs with completed feedback
-- transform akoma Ntoso to html
-- more concrete example of an extent
-- human readable description of enrichment
-- human readable enrichment feedback prompt


comment on view public_api.docs_with_outstanding_feedback is 'document table filter that returns documents that have ANY enrichments missing feedback';


alter view public_api.docs_with_outstanding_feedback owner to orp_postgrest_web;
grant select on public_api.docs_with_outstanding_feedback to orp_postgrest_web;

create or replace view public_api.docs_with_completed_feedback as
select *
from public_api.document d
where exists (
    select 1 from public_api.document_enrichment_feedback_status defs
    where defs.document_id = d.id
    and feedback_status = 'review_complete'
    and most_recent = true
);

comment on view public_api.docs_with_completed_feedback is 'document table filter that returns documents that have feedback on all enrichments';

alter view public_api.docs_with_completed_feedback owner to orp_postgrest_web;
grant select on public_api.docs_with_completed_feedback to orp_postgrest_web;
