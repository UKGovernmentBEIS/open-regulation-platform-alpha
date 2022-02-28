
begin;

select plan(2);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql


select update_document_metadata(id)
from public_api.document_metadata_definition;

-- \i tests/test_support/base-graph-setup.sql

select lives_ok($$
    select * from public_api.document_search(
        array[jsonb_populate_record(
            null::document_search_filter,
            '{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_name": "orpml_title",
                    "websearch_tsquery" : "asbestos"
                },
                {
                    "document_metadata_name": "orpml_classification",
                    "websearch_tsquery" : "asbestos"
                }]
            }'::jsonb
        )]
    ) ds
$$);


select lives_ok($$
    select * from public_api.document_search(
        array[jsonb_populate_record(
            null::document_search_filter,
            '{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_category": "title",
                    "websearch_tsquery" : "asbestos"
                },
                {
                    "document_metadata_category": "classification",
                    "websearch_tsquery" : "asbestos"
                }]
            }'::jsonb
        )]
    ) ds
$$);

rollback;