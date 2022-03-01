
begin;

select plan(3);

\i tests/test_support/base-users-setup.sql
\i tests/test_support/base-docs-setup.sql
\i tests/test_support/pgtap-doc-metadata-setup.sql

select lives_ok($$
    select register_event_type(
        'test_event','{key_a,key_b}'
    );
$$);

select lives_ok($$
    insert into public_api.event_subscription(
        event_type_id,
        event_filters,
        user_id
    )
    values (
        (select id from public_api.event_type where event_name = 'test_event'),
        array[
            ('key_a','value_a')::event_filter
        ]::event_filter[],
        (select id from users where email = 'editor@beis.gov.uk')
    );
$$);


select lives_ok($$
    select publish_event('test_event','{
        "key_a" : "value_a",
        "key_b" : "value_b"
    }');
$$);

rollback;