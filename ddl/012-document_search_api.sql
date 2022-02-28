
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

do $$
begin
    create type filter_operator_type as enum (
        'and','or'
    );
    exception when duplicate_object then null;
end $$;

do $$
begin
    create type filter_element_type as (
        filter_element_alias bigint,
        document_metadata_name text,
        document_metadata_category text,
        websearch_tsquery text
    );
    exception when duplicate_object then null;
end $$;

do $$
begin
    create type document_search_filter as (
        filter_element_alias bigint,
        operator filter_operator_type,
        filter_elements filter_element_type[]
    );
    exception when duplicate_object then null;
end $$;


create or replace function generate_document_search_query_py_types() returns void as
$$
    import uuid
    def alpha_erate(iterable):
        def ichar(n):
            assert n < 26
            return chr(ord('a')+n)

        for i,item in enumerate(iterable):
            yield ichar(i),item

    def generate_document_search_query(filters,temp_table_name,latest=True):
        # just use the first filter for now
        top_level_filter = filters[0]
        plpy.notice(f'{type(top_level_filter)}')
        plpy.notice(f'{top_level_filter}')

        search_filters = []
        # joins = []

        for alpha,fe in alpha_erate(top_level_filter['filter_elements']):
            element_filters = []
            if fe['document_metadata_category']:
                dm_cat = plpy.quote_literal(fe['document_metadata_category'])
                metadata_names = [plpy.quote_literal(n['name']) for n in plpy.execute(f"select name from public_api.document_metadata_definition where category = {dm_cat}")]
            else:
                metadata_names = [plpy.quote_literal(fe['document_metadata_name'])]

            for dm_name in metadata_names:
                dm_id = plpy.execute(f"select id from public_api.document_metadata_definition where name = {dm_name}")[0]['id']
                ts_conf = plpy.execute(f"select tsvector_config from public_api.document_metadata_definition where name = {dm_name}")[0]['tsvector_config']
                wbs_tsq = plpy.quote_literal(fe['websearch_tsquery'])
                element_filters.append(f"""
                    select document_id
                    from public_api.document_metadata
                    where
                    document_metadata_definition_id = {dm_id} and tsvec @@ websearch_to_tsquery('{ts_conf}',{wbs_tsq})
                    {'and latest is true' if latest else ''}
                """)

            union = 'union all\n'.join(element_filters)

            search_filters.append(f"""
                (
                    {union}
                ) {alpha} """
            )

        if top_level_filter['operator'] == 'and':
            filter_str = "\n".join([f" inner join {f} using (document_id)" if i > 0 else f for i,f in enumerate(search_filters)])
        elif top_level_filter['operator'] == 'or':
            raise NotImplementedError()
        elif top_level_filter['operator'] is None:
            assert len(search_filters) == 1
            filter_str = search_filters[0]

        query = f"""
            create temp table {temp_table_name} as
            select document_id
            from {filter_str}
        """

        plpy.notice(query)
        return query

    GD['generate_document_search_query'] = generate_document_search_query

$$ language plpython3u;


-- create or replace function public_api.document_search(
--     filters document_search_filter[]
-- ) returns setof bigint as
-- $$
-- declare
-- temp_table_name text;
-- begin
--     -- select 'document_search_' || replace(gen_random_uuid()::text,'-','_') into temp_table_name;
--     -- execute (select generate_document_search_query(filters,temp_table_name));
--     -- return query execute 'select * from ' || temp_table_name;
-- end;
-- $$ language plpgsql;

create or replace function public_api.document_search(
    filters document_search_filter[],
    only_latest boolean default true
) returns setof bigint as
$$
    import uuid
    if 'generate_document_search_query' not in GD:
        plpy.execute("select generate_document_search_query_py_types();")

    generate_document_search_query = GD['generate_document_search_query']
    temp_table_name = f"document_search_{str(uuid.uuid4()).replace('-','_')}"
    query = generate_document_search_query(filters,temp_table_name,only_latest)
    plpy.execute(query)
    return (r['document_id'] for r in plpy.execute(f"select * from {temp_table_name}"))
$$ language plpython3u;