
begin;

select plan(3);

\i tests/test_support/base-docs-setup.sql

select load_single_document(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/revisions/618_v2.xml'
);

select set_eq($$
    select revision_number,latest from public_api.document where pk = '/uksi/2002/618'
$$,
$$
    values (0,false),(1,true)
$$);

select throws_ok($$
    delete from public_api.document where pk = '/uksi/2002/618' and latest is false;
$$);

delete from public_api.document where pk = '/uksi/2002/618' and latest is true;

select set_eq($$
    select revision_number,latest from public_api.document where pk = '/uksi/2002/618'
$$,
$$
    values (0,true)
$$);

rollback;