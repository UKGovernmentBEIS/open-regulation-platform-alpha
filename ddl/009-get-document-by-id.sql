
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--r


-- create or replace function public_api.get_document_by_id(document_id bigint) returns json as
-- $$
-- declare
-- select_columns text;
-- enrichment_joins text;
-- enrichment_query text;
-- enrichments json;
-- begin

--     select string_agg(format($j$ left join %1$I_enrichment %1$s_ed on %1$I_ed.document_id = document.id $j$,type),E'\n') into enrichment_joins
--     from (
--         select distinct(type) as type
--         from public_api.enrichment_def
--     ) s;

--     select 'select json_build_object(' || string_agg(
--         format($e$
--             '%1$s_enrichments',json_agg(
--                 json_build_object(
--                     'enrichment_value',%1$I_ed.data,
--                     'enrichment_def_id',%1$I_ed.enrichment_def_id,
--                     'enrichment_extent',to_jsonb(%1$I_ed.extent),
--                     'enrichment_id',%1$I_ed.id
--                 )
--             ) $e$,type
--         ),E'\n'
--     ) || ')' into select_columns
--     from (select distinct(type) as type from public_api.enrichment_def) s;

--     raise notice '% %',select_columns,enrichment_joins;

--     select format($f$ %1$s from document %2$s where document_id = %3$L $f$,select_columns,enrichment_joins,document_id) into enrichment_query;

--     execute enrichment_query into enrichments;

--     return json_build_object(
--         'document_body',(select raw_text from document where id = document_id),
--         'document_type',(select name from document_type where id = (select document_type_id from document where id = document_id)),
--         'document_enrichments',enrichments
--     );
-- end;
-- $$ language plpgsql;

-- grant execute on function public_api.get_document_by_id(bigint) to orp_postgrest_web;