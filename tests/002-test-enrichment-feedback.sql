
begin;

select plan(6);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql

select ok(
    (select count(*) > 0 from public_api.document)
);

insert into public_api.enrichment_def (document_type_id,name,type,function_name)
values ((select id from public_api.document_type where name = 'legislation.gov.uk'),'deontic_language','text','deontic_language');

-- create a manual one to make sure some documents have multiple enrichments
insert into public_api.enrichment_def (document_type_id,name,type,is_manual)
values ((select id from public_api.document_type where name = 'legislation.gov.uk'),'labelled stuff','text',true);


insert into public_api.enrichment (
    document_id,
    enrichment_def_id,
    extent,
    data
)
select d.id,
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
from public_api.document d;


select update_enrichment_def(1,10000,100);

select ok(
    (select count(*) > 0 from public_api.enrichment)
);

select set_config('request.jwt.claim.user_id',(select id::text from users where email = 'editor@beis.gov.uk'),false);
set role orp_postgrest_web;

select lives_ok($$
    insert into public_api.enrichment_feedback
    (
        enrichment_id,
        good,
        notes
    )
    values (
        (
            select e.id from public_api.enrichment e
            inner join public_api.document d on e.document_id = d.id
            order by d.id limit 1
        ),
        true,
        'test'
    )
$$);

set constraints all immediate;

select throws_ok($$
    insert into public_api.document_enrichment_feedback_status (
        document_id,
        feedback_status
    )
    values (
        (select d.id from public_api.enrichment e
        inner join public_api.document d on e.document_id = d.id
        order by d.id limit 1),
        'review_complete'
    )
$$);

set role postgres;

select ok(
    (select count(*) = 1 from public_api.enrichment_feedback)
);

set role orp_postgrest_web;

-- mark all enrichments as good

insert into public_api.enrichment_feedback
(
    enrichment_id,
    good,
    notes
)
select id,
    true,
    'N/A'
from public_api.enrichment;

select lives_ok($$
    insert into public_api.document_enrichment_feedback_status (
        document_id,
        feedback_status
    )
    values (
        (select d.id from public_api.enrichment e
        inner join public_api.document d on e.document_id = d.id
        order by d.id limit 1),
        'review_complete'
    )
$$);




rollback;
