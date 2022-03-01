

begin;

select plan(2);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/base-orpml-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql

select lives_ok($$
    select update_document_metadata((select id from public_api.document_metadata_definition where name = 'legislation_title'));
$$);

select ok(
    (select count(*) > 0 from public_api.document_metadata)
);

rollback;
