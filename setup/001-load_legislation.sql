
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

-- create or replace function validate_akoma_ntoso(raw_text text) returns boolean as
-- $$
--     select xpath_exists('/ans:akomaNtoso/*',raw_text::xml, array[
--         array['ans','http://docs.oasis-open.org/legaldocml/ns/akn/3.0'],
--         array['dcns', 'http://purl.org/dc/elements/1.1/']
--     ]);
-- $$ language sql;

-- insert into public_api.document_type (name,format,document_validation_function) values ('legislation.gov.uk','xml','validate_akoma_ntoso');


-- select load_all_documents(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/ukla/',
--     max_docs => 50
-- );

\i tests/test_support/base-docs-setup.sql
