
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--


insert into public_api.enrichment_def (document_type_id,name,type,is_manual)
values ((select id from public_api.document_type where name = 'legislation.gov.uk'),'labelled stuff','text',true);

-- select update_enrichment_def((select id from public_api.enrichment_def where name = 'deontic_language'));
