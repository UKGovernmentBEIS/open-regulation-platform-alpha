

insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    function_name
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_html',
    'html',
    'akomantoso_to_html_dummy'
);


\i tests/test_support/common-doc-metadata-setup.sql