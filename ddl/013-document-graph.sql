
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

create table public_api.document_graph_relationship_definition (
    id bigint not null generated always as identity primary key,
    name text not null unique,
    document_metadata_definition_id_a bigint not null,
    document_metadata_definition_id_b bigint not null,
    document_metadata_definition_index_a text,
    document_metadata_definition_index_b text,
    query_template text not null,
    can_be_stale boolean not null default false,
    foreign key (document_metadata_definition_id_a) references public_api.document_metadata_definition(id) on update cascade on delete cascade,
    foreign key (document_metadata_definition_id_b) references public_api.document_metadata_definition(id) on update cascade on delete cascade
);

grant select on public_api.document_graph_relationship_definition to orp_postgrest_web;

create or replace function pyformat(s text,variables jsonb) returns text as
$$
    import json
    return s.format(**json.loads(variables))
$$ language plpython3u;


create or replace function distinct_pairs(ids bigint[]) returns table (
    id_a bigint,
    id_b bigint
) as
$$
    res = []
    for i,id_a in enumerate(ids):
        for j,id_b in enumerate(ids[i+1:]):
            res.append((id_a,id_b))
    return res
$$ language plpython3u;

create or replace function update_document_graph_relationship_definition(document_graph_relationship_definition_id bigint) returns void as
$$
declare
q text;
index_name_a text;
index_name_b text;
dgrd public_api.document_graph_relationship_definition;
_new_rows bigint;
begin

    select * into dgrd from public_api.document_graph_relationship_definition where id = document_graph_relationship_definition_id;

    if dgrd.document_metadata_definition_index_a is not null then
        select 'document_graph_relationship_definition_' || document_graph_relationship_definition_id || 'a' into index_name_a;
        if not exists (select 1 from pg_indexes where indexname = index_name_a) then
            select format($i$
                create index %1$I on public_api.document_metadata %3$s where document_metadata_definition_id = %2$L
            $i$,index_name_a,dgrd.document_metadata_definition_id_a,dgrd.document_metadata_definition_index_a) into q;
            raise notice '%',q;
            execute q;
        end if;
    end if;

    if dgrd.document_metadata_definition_index_b is not null then
        select 'document_graph_relationship_definition_' || document_graph_relationship_definition_id || 'b' into index_name_b;
        if not exists (select 1 from pg_indexes where indexname = index_name_b) then
            select format($i$
                create index %1$I on public_api.document_metadata %3$s where document_metadata_definition_id = %2$L
            $i$,index_name_b,dgrd.document_metadata_definition_id_b,dgrd.document_metadata_definition_index_b) into q;
            raise notice '%',q;
            execute q;
        end if;
    end if;


    select pyformat(
        dgrd.query_template,
        jsonb_build_object(
            'name',dgrd.name,
            'document_graph_relationship_definition_id',dgrd.id,
            'document_metadata_definition_id_a',dgrd.document_metadata_definition_id_a,
            'document_metadata_definition_id_b',dgrd.document_metadata_definition_id_b

        )
    ) into q;

    perform set_config('min_parallel_table_scan_size','1',false);
    perform set_config('min_parallel_index_scan_size','1',false);

    select format($t$
        drop table if exists graph_temp_%1$s;
        create temp table graph_temp_%1$s on commit drop as
        %2$s
    $t$,dgrd.id,q) into q;

    raise notice '%',q;
    execute q;

    select format($i$
        insert into public_api.document_graph (
            document_id_a,
            document_a_latest,
            document_a_revision_number,
            document_a_pk,
            document_id_b,
            document_b_latest,
            document_b_revision_number,
            document_b_pk,
            document_graph_relationship_definition_id,
            relationship_properties
        )
        select * from graph_temp_%1$s
        on conflict on constraint document_graph_unique do nothing;
    $i$,dgrd.id) into q;



    raise notice '%',q;

    execute q;

    get diagnostics _new_rows = ROW_COUNT;

    raise notice 'inserted % rows into the graph table',_new_rows;

end;
$$ language plpgsql;

create table public_api.document_graph (
    id bigint not null generated always as identity primary key,
    document_id_a bigint not null,
    document_a_latest boolean not null,
    document_a_revision_number bigint not null,
    document_a_pk text not null,
    document_id_b bigint not null,
    document_b_latest boolean not null,
    document_b_revision_number bigint not null,
    document_b_pk text not null,
    document_graph_relationship_definition_id bigint not null,
    relationship_properties jsonb not null,
    prop_hash bigint not null generated always as (hashtextextended(relationship_properties::text,2048)) stored,
    possibly_stale boolean,
    foreign key (document_id_a,document_a_latest) references public_api.document(id,latest) on update cascade on delete cascade,
    foreign key (document_id_b,document_b_latest) references public_api.document(id,latest) on update cascade on delete cascade,
    foreign key (document_id_a) references public_api.document(id) on update cascade on delete cascade, -- appear to need these as postgrest quite figure out the multi-column fk?
    foreign key (document_id_b) references public_api.document(id) on update cascade on delete cascade, -- appear to need these as postgrest quite figure out the multi-column fk?
    foreign key (document_graph_relationship_definition_id) references public_api.document_graph_relationship_definition(id) on update cascade on delete cascade,
    constraint document_graph_unique unique (document_id_a,document_id_b,document_graph_relationship_definition_id,prop_hash)
);

create index on public_api.document_graph(document_graph_relationship_definition_id);
create index on public_api.document_graph(document_id_a);
create index on public_api.document_graph(document_id_b);

create index on public_api.document_graph(document_a_pk,document_b_pk);

grant select on public_api.document_graph to orp_postgrest_web;



create or replace function document_graph_before_insert_trigger_f() returns trigger as
$$
declare
dgrd public_api.document_graph_relationship_definition;
begin
    select * into dgrd from public_api.document_graph_relationship_definition where id = new.document_graph_relationship_definition_id;

    if dgrd.can_be_stale is true then
        if exists (
            select 1 from public_api.document_graph dg
            where dg.document_a_pk = new.document_a_pk and dg.document_b_pk = new.document_b_pk
            and array[dg.document_a_revision_number,dg.document_b_revision_number] && array[new.document_a_revision_number,new.document_b_revision_number]
        ) then
            raise notice 'new relationship % may be stale',jsonb_pretty(row_to_json(new.*)::jsonb);
            select true into new.possibly_stale;
            -- new.possibly_stale := true;
            -- raise notice 'after %',jsonb_pretty(row_to_json(new.*)::jsonb);
        end if;
    end if;

    return new;
end;
$$ language plpgsql;

drop trigger if exists before_insert_trigger on public_api.document_graph;
create trigger before_insert_trigger before insert on public_api.document_graph
for each row
execute procedure document_graph_before_insert_trigger_f();

do $$
begin
    create type confirmationstatus as enum (
        'reconfirmed',
        'confirmed_stale'
    );
    exception when duplicate_object then null;
end $$;

create table if not exists public_api.document_graph_relationship_confirmation (
    id bigint generated by default as identity primary key,
    document_graph_id bigint not null,
    confirmation_status confirmationstatus not null,
    latest boolean not null default true,
    user_id bigint not null default current_setting('request.jwt.claim.user_id', true)::bigint,
    created_on timestamp not null default now(),
    foreign key (user_id) references users (id) on update cascade on delete cascade,
    foreign key (document_graph_id) references public_api.document_graph(id) on update cascade on delete cascade,
    constraint confirmation_one_latest exclude using gist(document_graph_id with =,(nullif(latest,false)::int) with =) deferrable initially deferred
);

alter table public_api.document_graph_relationship_confirmation enable row level security;
grant select,insert,update(latest) on public_api.document_graph_relationship_confirmation to orp_postgrest_web;

create policy public_api_s ON public_api.document_graph_relationship_confirmation for select to orp_postgrest_web using (
    (user_id=current_setting('request.jwt.claim.user_id', true)::bigint)
);

create policy public_api_user_u ON public_api.document_graph_relationship_confirmation for update to orp_postgrest_web using (
    user_id=current_setting('request.jwt.claim.user_id', true)::bigint
);

create policy public_api_user_i ON public_api.document_graph_relationship_confirmation for insert to orp_postgrest_web with check (
    user_id=current_setting('request.jwt.claim.user_id', true)::bigint
);

create or replace function document_graph_relationship_confirmation_after_insert_trigger_f() returns trigger as
$$
begin
    update public_api.document_graph_relationship_confirmation set latest = false where document_graph_id = new.document_graph_id and id != new.id;
    return new;
end;
$$ language plpgsql;

drop trigger if exists after_insert_trigger on public_api.document_graph_relationship_confirmation;
create trigger after_insert_trigger after insert on public_api.document_graph_relationship_confirmation
for each row
execute procedure document_graph_relationship_confirmation_after_insert_trigger_f();

select register_event_type(
    'stale_document_relationship',
    '{stale_document_pk,changed_document_pk}'::text[]
);

create or replace function document_graph_after_insert_trigger_f() returns trigger as
$$
declare
last_rel public_api.document_graph;
begin
    if new.possibly_stale is true then
        select * into last_rel from public_api.document_graph dg where dg.document_a_pk = new.document_a_pk and dg.document_b_pk = new.document_b_pk order by id desc limit 1;

        if last_rel.document_id_a = new.document_id_a then
            -- document_b changed
            perform publish_event(
                'stale_document_relationship',
                jsonb_build_object(
                    'stale_document_pk',new.document_a_pk,
                    'changed_document_pk',new.document_b_pk
                )
            );
        else
            -- document_a_changed
                perform publish_event(
                'stale_document_relationship',
                jsonb_build_object(
                    'stale_document_pk',new.document_b_pk,
                    'changed_document_pk',new.document_a_pk
                )
            );
        end if;
    end if;
    return new;
end;
$$ language plpgsql;

drop trigger if exists after_insert_trigger on public_api.document_graph;
create trigger after_insert_trigger after insert on public_api.document_graph
for each row
execute procedure document_graph_after_insert_trigger_f();

create or replace function generate_expand_from_doc_ids_query_py_types() returns void as
$$
    def generate_expand_from_doc_ids_query(doc_ids_expr,relationship_names,expand_from_doc_ids_temp_table,only_expand_from = None,only_latest = True):
        filters = []
        if relationship_names:
            names = ",".join([plpy.quote_literal(rn) for rn in relationship_names])
            filters.append(f"(document_graph_relationship_definition_id in (select id from public_api.document_graph_relationship_definition where name in ({names})))")

        if only_expand_from:
            filters.append(f"(document_id_a in {doc_ids_expr} and document_id_b in {doc_ids_expr}) or (doc_id in ({','.join(only_expand_from)}))")

        if only_latest:
            filters.append(f"((document_a_latest is true) and (document_b_latest is true))")

        filter_str = f"where {' and '.join(filters)}" if filters else ""

        query = f"""
            create temp table {expand_from_doc_ids_temp_table} as
            select json_agg(
                    distinct jsonb_build_object(
                        'data',jsonb_build_object(
                            'id',dg.id,
                            'source',dg.document_id_a,
                            'target',dg.document_id_b,
                            'property_key',(select key from jsonb_each(dg.relationship_properties)),
                            'properties',dg.relationship_properties,
                            'stale',(
                                case when (dg.possibly_stale is true and (dgrc.confirmation_status)::text is distinct from 'reconfirmed') then 'True' else 'False' end
                            ),
                            'relationship_confirmation',jsonb_build_object(
                                'confirmation_status',confirmation_status,
                                'user_id',dgrc.user_id,
                                'confirmed_on',dgrc.created_on
                            )
                        )
                    )
                ) as edges,
                array_agg(distinct doc_id) as nodes
            from {doc_ids_expr} tt
            inner join public_api.document_graph dg on tt.document_id = document_id_a or tt.document_id = document_id_b
            left join public_api.document_graph_relationship_confirmation dgrc on dgrc.document_graph_id = dg.id and dgrc.latest is true,
            lateral ( values (document_id_a),(document_id_b) ) s(doc_id)
            {filter_str}
        """

        plpy.notice(query)
        return query

    GD['generate_expand_from_doc_ids_query'] = generate_expand_from_doc_ids_query

$$ language plpython3u;

create or replace function generate_get_docs_with_metadata_py_types() returns void as
$$
    def generate_get_docs_with_metadata(doc_ids_expr,metadata_categories,docs_with_metadata_temp_table):

        assert len(metadata_categories) > 0

        metadata_cat_names = ",".join([plpy.quote_literal(mc) for mc in metadata_categories])

        query = f"""
            create temp table {docs_with_metadata_temp_table} as
            select jsonb_build_object(
                    'id',d.id,
                    'document_type_name',dt.name,
                    'document_type_id',dt.id
                ) || jsonb_object_agg(dmd.category,dm.data) as data
            from public_api.document d
            inner join public_api.document_type dt on d.document_type_id = dt.id
            inner join public_api.document_metadata dm on d.id = dm.document_id
            inner join public_api.document_metadata_definition dmd on dmd.id = dm.document_metadata_definition_id
            where d.id in (
                {doc_ids_expr}
            )
            and dm.document_metadata_definition_id in (
                select id from public_api.document_metadata_definition where category in ({metadata_cat_names})
            )
            group by d.id,dt.name,dt.id
        """

        plpy.notice(query)
        return query

    GD['generate_get_docs_with_metadata'] = generate_get_docs_with_metadata


$$ language plpython3u;


create or replace function public_api.graph_search(
    filters document_search_filter[],
    relationship_names text[],
    metadata_categories text[]
) returns jsonb as
$$
    import uuid
    if 'generate_document_search_query' not in GD:
        plpy.execute("select generate_document_search_query_py_types();")
    if 'generate_expand_from_doc_ids_query' not in GD:
        plpy.execute("select generate_expand_from_doc_ids_query_py_types();")
    if 'generate_get_docs_with_metadata' not in GD:
        plpy.execute("select generate_get_docs_with_metadata_py_types();")

    # perform a search to get back an initial node list
    generate_document_search_query = GD['generate_document_search_query']
    initial_search_temp_table_name = f"document_search_{str(uuid.uuid4()).replace('-','_')}"
    search = generate_document_search_query(filters,initial_search_temp_table_name)
    plpy.execute(search)

    # get the nodes and edges after a one hop expansion along the specified relationship types
    generate_expand_from_doc_ids_query = GD['generate_expand_from_doc_ids_query']
    expand_from_doc_ids_temp_table = f"expand_from_doc_ids_{str(uuid.uuid4()).replace('-','_')}"
    search = generate_expand_from_doc_ids_query(initial_search_temp_table_name,relationship_names,expand_from_doc_ids_temp_table)
    plpy.execute(search)


    # get the metadata for the returned nodes
    doc_ids_expr = f"""
        select n from
        {expand_from_doc_ids_temp_table},
        lateral unnest(nodes) n
    """

    generate_get_docs_with_metadata = GD['generate_get_docs_with_metadata']
    docs_with_metadata_temp_table = f"docs_with_metadata_{str(uuid.uuid4()).replace('-','_')}"
    search = generate_get_docs_with_metadata(doc_ids_expr,metadata_categories,docs_with_metadata_temp_table)
    plpy.execute(search)

    nodes = plpy.execute(f"select json_agg(row_to_json(f.*)) as nodes from {docs_with_metadata_temp_table} f")[0]['nodes']
    edges = plpy.execute(f"select edges from {expand_from_doc_ids_temp_table} e")[0]['edges']

    return f"""{{
        "nodes" : {nodes or '[]'},
        "edges" : {edges or '[]'}
    }}"""
$$ language plpython3u;


create or replace function public_api.traverse_from_doc_ids(
    doc_ids bigint[],
    relationship_names text[],
    metadata_categories text[]
) returns jsonb as
$$
    import uuid
    if 'generate_expand_from_doc_ids_query' not in GD:
        plpy.execute("select generate_expand_from_doc_ids_query_py_types();")
    if 'generate_get_docs_with_metadata' not in GD:
        plpy.execute("select generate_get_docs_with_metadata_py_types();")

    # put docs_ids into temp_table
    doc_id_str = ','.join([f"({d})" for d in doc_ids])
    initial_search_temp_table_name = f"document_search_{str(uuid.uuid4()).replace('-','_')}"
    search = f"create temp table {initial_search_temp_table_name} as select * from (values {doc_id_str}) as v(document_id)"
    plpy.notice(search)
    plpy.execute(search)

    # get the nodes and edges after a one hop expansion along the specified relationship types
    generate_expand_from_doc_ids_query = GD['generate_expand_from_doc_ids_query']
    expand_from_doc_ids_temp_table = f"expand_from_doc_ids_{str(uuid.uuid4()).replace('-','_')}"
    search = generate_expand_from_doc_ids_query(initial_search_temp_table_name,relationship_names,expand_from_doc_ids_temp_table)
    plpy.execute(search)


    # get the metadata for the returned nodes
    doc_ids_expr = f"""
        select *
        from {initial_search_temp_table_name}
        union (
            select n
            from {expand_from_doc_ids_temp_table},
            lateral unnest(nodes) n
        )
    """

    generate_get_docs_with_metadata = GD['generate_get_docs_with_metadata']
    docs_with_metadata_temp_table = f"docs_with_metadata_{str(uuid.uuid4()).replace('-','_')}"
    search = generate_get_docs_with_metadata(doc_ids_expr,metadata_categories,docs_with_metadata_temp_table)
    plpy.execute(search)

    nodes = plpy.execute(f"select json_agg(row_to_json(f.*)) as nodes from {docs_with_metadata_temp_table} f")[0]['nodes']
    edges = plpy.execute(f"select edges from {expand_from_doc_ids_temp_table} e")[0]['edges']

    return f"""{{
        "nodes" : {nodes},
        "edges" : {edges or '[]'}
    }}"""
$$ language plpython3u;