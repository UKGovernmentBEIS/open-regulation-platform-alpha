
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--



do $$
begin
    create type extent_type as enum ('xml', 'html');
    exception when duplicate_object then null;
end $$;

do $$
begin
    create type extent_section as (
        extent_start text,
        extent_end text,
        extent_char_start bigint,
        extent_char_end bigint
    );
    exception when duplicate_object then null;
end $$;

do $$
begin
    create type document_extent as (
        type extent_type,
        sections extent_section[]
    );
    exception when duplicate_object then null;
end $$;

create table public_api.document_metadata_definition(
    id bigint not null generated always as identity primary key,
    id_highwater_mark bigint not null default 0,
    document_type_id bigint not null,
    name text not null unique,
    category text not null,
    transform_xpath text,
    function_name text,
    tsvector_config text,
    distinctify boolean not null default false,
    foreign key (document_type_id) references public_api.document_type(id) on update cascade on delete cascade,
    constraint unique_cat_per_dtid unique(document_type_id,category)
);

comment on table public_api.document_metadata_definition is 'Defines the document metadata extraction process for a document type, and any text search config on the output data';

grant select on public_api.document_metadata_definition to orp_postgrest_web;


create or replace function document_metadata_definition_after_insert_or_update_trigger_f() returns trigger as
$$
declare
q text;
begin
    if new.tsvector_config is not null then
        select format($i$
            create index if not exists document_metadata_tsvector_%1$s on public_api.document_metadata using gin (tsvec) where document_metadata_definition_id = %1$L
        $i$,new.id) into q;
        raise notice '%',q;
        execute q;
    end if;
    return new;
end;
$$ language plpgsql;

drop trigger if exists after_insert_trigger on public_api.document_metadata_definition;
create trigger after_insert_trigger after insert or update on public_api.document_metadata_definition
for each row
execute procedure document_metadata_definition_after_insert_or_update_trigger_f();


create table public_api.distinct_document_metadata (
    id bigint not null generated always as identity primary key,
    document_metadata_definition_id bigint not null,
    data text not null,
    tsvec tsvector,
    _hash text not null generated always as (hashtextextended(data,2048)) stored,
    foreign key (document_metadata_definition_id) references public_api.document_metadata_definition(id) on update cascade on delete cascade,
    constraint unique_per_dmd unique(document_metadata_definition_id,_hash)
);

grant select on public_api.distinct_document_metadata to orp_postgrest_web;
create index on public_api.distinct_document_metadata(document_metadata_definition_id) include(id,data);

comment on table public_api.distinct_document_metadata is 'The list of distinct metadata values for that definition, if it is defined as distinctified';

create table public_api.document_metadata (
    id bigint not null generated always as identity primary key,
    document_metadata_definition_id bigint not null,
    document_id bigint not null,
    latest boolean not null,
    revision_number bigint not null,
    pk text not null,
    data text,
    tsvec tsvector,
    extent document_extent,
    error jsonb,
    foreign key (document_id,latest) references public_api.document(id,latest) on update cascade on delete cascade,
    foreign key (document_metadata_definition_id) references public_api.document_metadata_definition(id) on update cascade on delete cascade
);

create index on public_api.document_metadata(document_metadata_definition_id);
grant select on public_api.document_metadata to orp_postgrest_web;

comment on table public_api.document_metadata is 'The individual values of document metadata for a document and document_metadata_definition, when text search vector';


create table public_api.distinct_document_metadata_document (
    id bigint not null generated always as identity primary key,
    distinct_document_metadata_id bigint not null,
    document_metadata_id bigint not null,
    foreign key (document_metadata_id) references public_api.document_metadata(id) on update cascade on delete cascade,
    foreign key (distinct_document_metadata_id) references public_api.distinct_document_metadata(id) on update cascade on delete cascade
);

create index on public_api.distinct_document_metadata_document(document_metadata_id) include(distinct_document_metadata_id);
grant select on public_api.distinct_document_metadata_document to orp_postgrest_web;

comment on table public_api.distinct_document_metadata_document is 'Association table between document metadata values and the id of their distinct value';

create or replace function document_metadata_after_insert_trigger_f() returns trigger as
$$
declare
q text;
dmd_id bigint;
tsvec_config text;
distinctify boolean;
begin
    select document_metadata_definition_id into dmd_id from new limit 1;
    select tsvector_config,dmd.distinctify into tsvec_config,distinctify from public_api.document_metadata_definition dmd where id = dmd_id;

    if distinctify then
        insert into public_api.distinct_document_metadata (data,tsvec,document_metadata_definition_id)
        select data,
            case when tsvec_config is not null then to_tsvector(tsvec_config::regconfig,data) else null end,
            dmd_id
        from new
        on conflict on constraint unique_per_dmd do nothing;

        insert into public_api.distinct_document_metadata_document (distinct_document_metadata_id,document_metadata_id)
        select dimd.id,n.id
        from public_api.distinct_document_metadata dimd
        inner join new n on n.data = dimd.data
        where dimd.document_metadata_definition_id = dmd_id;
    end if;

    if tsvec_config is not null then
        raise notice 'updating tsvector data for document_metadata id %',dmd_id;
        select format($u$
            update public_api.document_metadata dm
            set tsvec = to_tsvector(%1$L,dm.data)
            from new where new.id = dm.id
        $u$,tsvec_config) into q;
        raise notice '%',q;
        execute q;
    end if;
    return new;
end;
$$ language plpgsql;

drop trigger if exists after_insert_trigger on public_api.document_metadata;
create trigger after_insert_trigger after insert on public_api.document_metadata
referencing new table as new
for each statement
execute procedure document_metadata_after_insert_trigger_f();

create index on public_api.document_metadata(document_id);
create index on public_api.document_metadata(document_metadata_definition_id);

grant select on public_api.document_metadata to orp_postgrest_web;


create view public_api.document_metadata_view as
select dm.*,dmd.name,dmd.category,ddmd.distinct_document_metadata_id as distinct_metadata_id
from public_api.document_metadata dm
inner join public_api.document_metadata_definition dmd on dmd.id = dm.document_metadata_definition_id
left join public_api.distinct_document_metadata_document ddmd on ddmd.document_metadata_id = dm.id;

alter view public_api.document_metadata_view owner to orp_postgrest_web;
grant select on public_api.document_metadata_view to orp_postgrest_web;

comment on view public_api.document_metadata_view is 'A view that enables retrieval and filtering of document_metadata values filters by document_metadata_defintion name, primarily to make the postgrest API easier';

create view public_api.distinct_document_metadata_view as
select ddm.*,dmd.name,dmd.category
from public_api.distinct_document_metadata ddm
inner join public_api.document_metadata_definition dmd on dmd.id = ddm.document_metadata_definition_id;

alter view public_api.distinct_document_metadata_view owner to orp_postgrest_web;
grant select on public_api.distinct_document_metadata_view to orp_postgrest_web;

comment on view public_api.distinct_document_metadata_view is 'A view that enables retreival and filtering of distinct_document_metadata values filters by document_metadata_defintion name, primarily to make the postgrest API easier (e.g. taxomonies)';



create or replace function update_document_metadata(document_metadata_definition_id bigint) returns void as
$$
declare
q text;
new_max_id bigint;
_new_rows bigint;
current_max_id bigint;
dmd public_api.document_metadata_definition;
dt public_api.document_type;
start_time timestamp;
elapsed numeric;
begin
    -- lock this metadata_defintion_id
    select * into dmd from public_api.document_metadata_definition where id = document_metadata_definition_id for no key update;

    select * into dt from public_api.document_type where id = dmd.document_type_id;

    select coalesce(max(id),0) into new_max_id
    from public_api.document
    where document_type_id = dmd.document_type_id;

    select dmd.id_highwater_mark into current_max_id;

    perform set_config('parallel_setup_cost','0',false);
    perform set_config('parallel_tuple_cost','0',false);
    perform set_config('min_parallel_table_scan_size','1kB',false);
    perform set_config('min_parallel_index_scan_size','1kB',false);

    execute format('drop table if exists metadata_temp_%1$s',dmd.id);

    if dmd.transform_xpath is not null then
        select format($m$
            create temp table metadata_temp_%1$s on commit drop as
            select dmd_id,
                doc_id,
                latest,
                revision_number,
                pk,
                xpath_value as data,
                null::document_extent as extent,
                null::jsonb as error
            from (
                select %1$L::bigint as dmd_id,
                    id as doc_id,
                    latest,
                    revision_number,
                    pk,
                    xpath(
                        %4$L,
                        raw_text::xml,
                        %5$L
                    ) as x
                from public_api.document
                where id > %2$L and id <= %3$L
                and document_type_id = %6$L
            ) s,
            lateral unnest(x) as xpath_value
            where x is not null;
        $m$,dmd.id,current_max_id,new_max_id,dmd.transform_xpath,dt.xml_ns,dt.id) into q;

    elsif dmd.function_name is not null then
        select format($i$
            create temp table metadata_temp_%1$s on commit drop as
            select %1$L::bigint,
                id as doc_id,
                latest,
                revision_number,
                pk,
                md.data,
                md.extent,
                md.error
            from public_api.document,
            lateral %2$I(raw_text) md
            where id > %3$L and id <= %4$L
            and document_type_id = %5$L
        $i$,dmd.id,
        dmd.function_name,current_max_id,new_max_id,dt.id) into q;
    else
        raise notice 'dmd - %',jsonb_pretty(row_to_json(dmd.*)::jsonb);
    end if;

    raise notice '%',q;

    select clock_timestamp() into start_time;
    execute q;

    get diagnostics _new_rows = ROW_COUNT;
    select extract(epoch from (clock_timestamp() - start_time)) into elapsed;
    raise notice '% rows generated in % seconds',_new_rows,elapsed;

    select format($i$
        insert into public_api.document_metadata (
            document_metadata_definition_id,
            document_id,
            latest,
            revision_number,
            pk,
            data,
            extent,
            error
        )
        select * from metadata_temp_%1$s
    $i$,dmd.id) into q;

    raise notice '%',q;

    select clock_timestamp() into start_time;
    execute q;

    get diagnostics _new_rows = ROW_COUNT;
    select extract(epoch from (clock_timestamp() - start_time)) into elapsed;
    raise notice '% rows loaded in % seconds',_new_rows,elapsed;

    update public_api.document_metadata_definition set id_highwater_mark = new_max_id where id = document_metadata_definition_id;

end;
$$ language plpgsql strict;
