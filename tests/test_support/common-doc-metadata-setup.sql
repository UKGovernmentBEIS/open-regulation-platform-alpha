




insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath,
    tsvector_config
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_title',
    'title',
    '/ans:akomaNtoso/ans:act/ans:meta/ans:proprietary/dcns:title/text()',
    'simple'
);


insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath,
    tsvector_config

)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_longtitle',
    'longtitle',
    '/ans:akomaNtoso/ans:act/ans:preface/ans:longTitle/ans:p/text()',
    'simple'
);



insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_identification',
    'identification',
    '/ans:akomaNtoso/ans:act/ans:meta/ans:identification/ans:FRBRWork/ans:FRBRthis/@value'
);


insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_enacted',
    'enacted',
    '/ans:akomaNtoso/ans:act/ans:meta/ans:identification/ans:FRBRWork/ans:FRBRdate/@date'
);

insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath,
    tsvector_config,
    distinctify
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_classification',
    'classification',
    '/ans:akomaNtoso/ans:act/ans:meta/ans:classification/ans:keyword/@value',
    'simple',
    true
);




insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    function_name,
    tsvector_config
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_raw_text',
    'raw_text',
    'xml_text',
    'simple'
);

insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    function_name,
    tsvector_config,
    distinctify
)
values (
    (select id from public_api.document_type where name = 'legislation.gov.uk'),
    'legislation_named_entities',
    'named_entities',
    'named_entity_extraction',
    'simple',
    true
);


insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath,
    tsvector_config,
    distinctify
)
values (
    (select id from public_api.document_type where name = 'orpml'),
    'orpml_title',
    'title',
    '/ans:akomaNtoso/ans:doc/@name',
    'simple',
    true
);


insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath,
    tsvector_config,
    distinctify
)
values (
    (select id from public_api.document_type where name = 'orpml'),
    'orpml_classification',
    'classification',
    '/ans:akomaNtoso/ans:doc/ans:meta/ans:classification/ans:keyword/@value',
    'simple',
    true
);




insert into public_api.document_metadata_definition(
    document_type_id,
    name,
    category,
    transform_xpath,
    tsvector_config,
    distinctify
)
values (
    (select id from public_api.document_type where name = 'orpml'),
    'orpml_legislation_link',
    'legislation_cited',
    '/ans:akomaNtoso/ans:doc/ans:mainBody/ans:foreign/orpml:guidance/orpml:body/orpml:guidance_block/@regulation',
    'simple',
    true
);



-- /ans:akomaNtoso/ans:classification/ans:keyword/@value


-- insert into public_api.document_metadata_definition(
--     document_type_id,
--     name,
--     function_name
-- )
-- values (
--     (select id from public_api.document_type where name = 'legislation.gov.uk'),
--     'legislation_raw_tsvector',
--     'ts_vector_from_xml'
-- );