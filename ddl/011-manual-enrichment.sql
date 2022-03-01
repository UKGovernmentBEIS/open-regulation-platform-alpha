
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

-- create or replace function public_api.manual_content_enrichment(
--     document_id bigint,
--     enrichment_def_id bigint,
--     extent document_extent,
--     data jsonb
-- ) returns void as
-- $$
-- declare
-- q text;
-- _new_rows bigint;
-- begin

--     select format($i$
--         insert into %1$I_enrichment (
--             document_id,
--             enrichment_def_id,
--             extent,
--             data
--         )
--         values
--         (
--             %2$L::bigint,
--             %3$L::bigint,
--             %4$L::document_extent,
--             %5$L::%1$I
--         )
--     $i$,(select type from public_api.enrichment_def where id = manual_content_enrichment.enrichment_def_id),
--     manual_content_enrichment.document_id,
--     manual_content_enrichment.enrichment_def_id,
--     manual_content_enrichment.extent,
--     (select format('%s',btrim((manual_content_enrichment.data)::text,'"')))
--     ) into q;

--     raise notice '%',q;
--     begin
--         execute q;
--     exception when insufficient_privilege then
--         raise exception using message = 'permission denied to create manual content enrichment';
--     end;

--     get diagnostics _new_rows = ROW_COUNT;
--     raise notice '% new rows',_new_rows;
-- end;
-- $$ language plpgsql;

-- grant execute on function public_api.manual_content_enrichment(bigint,bigint,document_extent,jsonb) to orp_postgrest_web;