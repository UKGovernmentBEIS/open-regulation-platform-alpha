
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--


\i tests/test_support/base-doc-metadata-setup.sql


-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'title'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'longtitle'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'enacted'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'identification'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'classification'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'legislation_raw_text'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'legislation_named_entities'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'html'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'legislation_html'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'legislation_raw_tsvector'));


-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'orpml_title'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'orpml_classification'));
-- select update_document_metadata((select id from public_api.document_metadata_definition where name = 'orpml_legislation_link'));

select update_document_metadata(id) from public_api.document_metadata_definition;


insert into public_api.enrichment_def (document_metadata_definition_id,name,type,function_name)
values ((select id from public_api.document_metadata_definition where name = 'legislation_html'),'deontic_language','text','deontic_language');

select update_enrichment_def((select id from public_api.enrichment_def where name = 'deontic_language'));


-- Named Entity

insert into public_api.enrichment_def (document_metadata_definition_id,name,type,function_name)
values ((select id from public_api.document_metadata_definition where name = 'legislation_html'),'named_entity_extraction','text','named_entity_extraction');

select update_enrichment_def((select id from public_api.enrichment_def where name = 'named_entity_extraction'));


