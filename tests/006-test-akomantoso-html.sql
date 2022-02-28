
begin;

select plan(1);

select lives_ok($$
    select akomaNtoso_to_html(raw_text) from public_api.document where document_type_id = 1 limit 1;
$$);

rollback;