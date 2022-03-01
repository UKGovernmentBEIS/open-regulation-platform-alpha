
begin;

select plan(3);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql

select update_document_metadata(id) from public_api.document_metadata_definition where category != 'html';

select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

insert into public_api.event_subscription (
    event_type_id,
    event_filters
)
values (
    (select id from public_api.event_type where event_name = 'new_document_revision'),
    array[
        ('document_pk','/uksi/2002/618')::event_filter
    ]::event_filter[]
);

set role postgres;

select load_single_document(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/revisions/618_v2.xml'
);


-- should be one event as editor
select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

select results_eq($$
    select count(*)::bigint from public_api.event_stream
$$,
$$
    values(1::bigint)
$$
);

set role postgres;


-- should be zero events as anon
select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'anonymous@beis.gov.uk'),false);
set role orp_postgrest_web;

select results_eq($$
    select count(*)::bigint from public_api.event_stream
$$,
$$
    values(0::bigint)
$$
);

set role postgres;

select load_single_document(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/revisions/618_v2.xml'
);


-- should still be one event as editor
select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

select results_eq($$
    select count(*)::bigint from public_api.event_stream
$$,
$$
    values(1::bigint)
$$
);


rollback;