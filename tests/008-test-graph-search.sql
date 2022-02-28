
begin;

select plan(3);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql


select update_document_metadata(id)
from public_api.document_metadata_definition;

\i tests/test_support/base-graph-setup.sql

select lives_ok($$
    select jsonb_pretty(ds) from public_api.graph_search(
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
        )],
        array['guidance_references_legislation']::text[],array['title','orpml_title']::text[]
    ) ds
$$);


select lives_ok($$
    select jsonb_pretty(ds) from public_api.graph_search(
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
        )],
        array['guidance_references_legislation']::text[],array['title','orpml_title']::text[]
    ) ds
$$);

select lives_ok($$
    select jsonb_pretty(ds) from public_api.traverse_from_doc_ids(
        array[(select id from public_api.document limit 1)],
        array[]::text[],array['title','orpml_title']::text[]
    ) ds;
$$);

rollback;