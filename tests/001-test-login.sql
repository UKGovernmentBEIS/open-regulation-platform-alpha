
begin;

select plan(2);


\i tests/test_support/base-users-setup.sql

select ok(
    (select j::jsonb ? 'signed_jwt' from public_api.login('anonymous@beis.gov.uk','Password1!') j)
);

select ok(
    (select j::jsonb ? 'message' from public_api.login('anonymous@beis.gov.uk','Password1!asdf') j)
);

rollback;
