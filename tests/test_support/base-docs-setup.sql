
-- insert into public_api.document_type (name,format) values ('legislation.gov.uk','xml');

-- select load_all_documents(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/',
--     max_docs => 100
-- );


-- insert into public_api.document_type (name,format) values ('orpml','xml');

-- select load_all_documents(
--     (select id from public_api.document_type where name = 'orpml'),
--     '/data/guidance/',
--     max_docs => 100
-- );

create or replace function validate_akoma_ntoso(raw_text text) returns boolean as
$$
    select xpath_exists('/ans:akomaNtoso/*',raw_text::xml, array[
        array['ans','http://docs.oasis-open.org/legaldocml/ns/akn/3.0'],
        array['dcns', 'http://purl.org/dc/elements/1.1/']
    ]);
$$ language sql;

create or replace function legislation_pk(doc text,dt public_api.document_type) returns text as
$$
    select (regexp_match(
        (xpath('/ans:akomaNtoso/ans:act/ans:meta/ans:identification/ans:FRBRWork/ans:FRBRthis/@value',doc::xml,dt.xml_ns))[1]::text,
        '/\w{2,5}/\d{4}/\d{1,5}'
    ))[1];
$$ language sql;

insert into public_api.document_type (
    name,
    format,
    document_validation_function,
    pk_function,
    xml_ns
) values (
    'legislation.gov.uk',
    'xml',
    'validate_akoma_ntoso',
    'legislation_pk',
    array[
        array['ans','http://docs.oasis-open.org/legaldocml/ns/akn/3.0'],
        array['dcns', 'http://purl.org/dc/elements/1.1/']
    ]
);

-- select load_single_document(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/legislation/uksi/2012/632.xml'
-- );

-- select load_single_document(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/legislation/uksi/2002/618.xml'
-- );

-- select load_single_document(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/legislation/uksi/2010/2984.xml'
-- );

select load_all_documents(
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    '/demo_data/legislation/',
    max_docs => 1000
);

-- select load_single_document(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/uksi/2012/632.xml'
-- );

-- select load_single_document(
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     '/data/uksi/2002/618.xml'
-- );

create or replace function guidance_pk(doc text,dt public_api.document_type) returns text as
$$
    select (xpath('/ans:akomaNtoso/ans:doc/@name',doc::xml,dt.xml_ns))[1]::text;
$$ language sql;

insert into public_api.document_type (
    name,
    format,
    pk_function,
    xml_ns
) values (
    'orpml',
    'xml',
    'guidance_pk',
    array[
        array['ans','http://docs.oasis-open.org/legaldocml/ns/akn/3.0'],
        array['dcns', 'http://purl.org/dc/elements/1.1/'],
        array['orpml','https://beis.gov.uk/schemas/orpml']
    ]
);

select load_all_documents(
    (select id from public_api.document_type where name = 'orpml'),
    '/demo_data/guidance/',
    max_docs => 100
);
