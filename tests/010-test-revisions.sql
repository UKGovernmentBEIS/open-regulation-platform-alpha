
begin;

select plan(5);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql

select update_document_metadata(id) from public_api.document_metadata_definition where category != 'html';

select results_eq($$
    select count(*)::bigint from (select count(*) from public_api.document group by pk ) s where count = 2
$$,
$$
    values (0::bigint)
$$);

select results_eq($$
    select count(*)>0 from public_api.document_metadata
    where document_id in (select id from public_api.document where pk = '/uksi/2002/618') and latest is true;
$$,
$$
    values (true)
$$);

select load_single_document(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/revisions/618_v2.xml'
);

-- original metadata should all be stale
select results_eq($$
    select count(*)=0 from public_api.document_metadata
    where document_id in (select id from public_api.document where pk = '/uksi/2002/618') and latest is true;
$$,
$$
    values (true)
$$);

select results_eq($$
    select count(*)::bigint from (select count(*) from public_api.document group by pk ) s where count = 2
$$,
$$
    values (1::bigint)
$$);

-- load again to esnure no new revision created
select load_single_document(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/revisions/618_v2.xml'
);

select results_eq($$
    select count(*)::bigint from (select count(*) from public_api.document group by pk ) s where count = 2
$$,
$$
    values (1::bigint)
$$);


rollback;