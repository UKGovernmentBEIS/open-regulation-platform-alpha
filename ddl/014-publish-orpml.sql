
--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

create or replace function public_api.publish_orpml(document jsonb) returns bigint as
$$
    insert into public_api.document(
        document_type_id,
        raw_text
    )
    values (
        (select id from public_api.document_type where name = 'orpml'),
        publish_orpml.document
    ) returning id;
$$ language sql security definer;

grant execute on function public_api.publish_orpml(jsonb) to orp_postgrest_web;