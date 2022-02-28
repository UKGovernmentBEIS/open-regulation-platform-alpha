
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

-- create or replace function public_api.enrichment_feedback(enrichment_def_id bigint,enrichment_id bigint,good boolean,notes text) returns void as
-- $$
-- declare
-- q text;
-- _new_rows bigint;
-- begin

--     select format($i$
--         insert into %1$I_enrichment_feedback (%1$I_enrichment_id,good,notes)
--         values
--         (%2$L::bigint,%3$L::boolean,%4$L::text)
--     $i$,(select type from public_api.enrichment_def where id = enrichment_feedback.enrichment_def_id),
--     enrichment_feedback.enrichment_id,
--     enrichment_feedback.good,
--     enrichment_feedback.notes
--     ) into q;

--     raise notice '%',q;
--     begin
--         execute q;
--     exception when insufficient_privilege then
--         raise exception using message = 'permission denied to provide enrichment feedback';
--     end;

--     get diagnostics _new_rows = ROW_COUNT;
--     raise notice '% new rows',_new_rows;
-- end;
-- $$ language plpgsql;

-- grant execute on function public_api.enrichment_feedback to orp_postgrest_web;