
begin;

select plan(4);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql


select update_document_metadata(id)
from public_api.document_metadata_definition;

\i tests/test_support/base-graph-setup.sql

select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

insert into public_api.event_subscription (
    event_type_id,
    event_filters
)
values (
    (select id from public_api.event_type where event_name = 'stale_document_relationship'),
    array[
        ('changed_document_pk','/uksi/2002/618')::event_filter
    ]::event_filter[]
);

set role postgres;

select load_single_document(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/revisions/618_v2.xml'
);

select update_document_metadata(id)
from public_api.document_metadata_definition;


select update_document_graph_relationship_definition((select id from public_api.document_graph_relationship_definition where name = 'guidance_references_legislation'));


select results_eq(
$$
    select count(*)::bigint from public_api.document_graph where possibly_stale is true;
$$,
$$
    values (1::bigint)
$$
);


select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

select results_eq($$
    select count(*)::bigint from public_api.event_stream
$$,
$$
    values(1::bigint)
$$
);

select results_eq($$
    select (ds->'edges'->0->'data'->>'stale')::boolean from public_api.graph_search(
        array[jsonb_populate_record(
            null::document_search_filter,
            '{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_name": "orpml_title",
                    "websearch_tsquery" : "medical"
                }]
            }'::jsonb
        )],
        array['guidance_references_legislation']::text[],array['title','orpml_title']::text[]
    ) ds
$$,
$$
    values (true)
$$);


select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;


insert into public_api.document_graph_relationship_confirmation (
    document_graph_id,
    confirmation_status
)
values (
    (select id from public_api.document_graph where possibly_stale is true),
    'reconfirmed'
);

select results_eq($$
    select (ds->'edges'->0->'data'->>'stale')::boolean from public_api.graph_search(
        array[jsonb_populate_record(
            null::document_search_filter,
            '{
                "operator" : "and",
                "filter_elements" : [{
                    "document_metadata_name": "orpml_title",
                    "websearch_tsquery" : "medical"
                }]
            }'::jsonb
        )],
        array['guidance_references_legislation']::text[],array['title','orpml_title']::text[]
    ) ds
$$,
$$
    values (false)
$$);

rollback;