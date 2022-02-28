--
-- Copyright (C) Analytics Engines
-- 2021 Lauren Stephens (l.stephens@analyticsengines.com)
--


-- insert into public_api.enrichment_def (document_type_id,name,type,function_name)
-- values ((select id from public_api.document_type where name = 'html'),'named_entity_extraction','text','named_entity_extraction');


-- select update_enrichment_def((select id from public_api.enrichment_def where name = 'named_entity_extraction'));

