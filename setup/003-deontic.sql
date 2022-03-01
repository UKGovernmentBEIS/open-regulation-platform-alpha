
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

-- insert into public_api.enrichment_def (document_metadata_definition_id,name,type,function_name)
-- values ((select id from public_api.document_metadata_definition where name = 'html'),'deontic_language','text','deontic_language');

-- select update_enrichment_def((select id from public_api.enrichment_def where name = 'deontic_language'));
