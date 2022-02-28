
begin;

select plan(2);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql


insert into public_api.enrichment_def (document_type_id,name,type,is_manual)
values ((select id from public_api.document_type where name = 'legislation.gov.uk'),'labelled stuff','text',true);

select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

select results_eq($$
    (select count(*)::bigint from public_api.unenriched_docs((select id from public_api.enrichment_def where name = 'labelled stuff')))
$$,
$$
    values (412::bigint)
$$
);

insert into public_api.enrichment (
    document_id,
    enrichment_def_id,
    extent,
    data
)
values (
    (select ud.id from public_api.unenriched_docs((select id from public_api.enrichment_def where name = 'labelled stuff')) ud limit 1),
    (select id from public_api.enrichment_def where name = 'labelled stuff'),
    jsonb_populate_record(
        null::document_extent,
        '{
            "type" : "xml",
            "sections" : [
                {
                    "extent_start" : "/body/section[1]",
                    "extent_end" : "/body/section[1]",
                    "extent_char_start" : null,
                    "extent_char_end" : null
                }
            ]
        }'::jsonb
    ),
    'section 1!'
);

select results_eq(
$$
    (select count(*)::bigint from public_api.unenriched_docs((select id from public_api.enrichment_def where name = 'labelled stuff')))
$$,
$$
    values (411::bigint)
$$
);


rollback;
