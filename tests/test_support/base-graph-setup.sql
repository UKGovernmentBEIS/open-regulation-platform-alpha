

insert into public_api.document_graph_relationship_definition (
    name,
    document_metadata_definition_id_a,
    document_metadata_definition_id_b,
    query_template
)
values (
    'legislation_cited_in',
    (select id from public_api.document_metadata_definition where name = 'legislation_title'),
    (select id from public_api.document_metadata_definition where name = 'legislation_raw_text'),
    $q$
        select dm_a_title.document_id as doc_id_a,
            dm_a_title.latest as doc_a_latest,
            dm_a_title.revision_number as doc_a_revision_number,
            dm_a_title.pk as doc_a_pk,
            dm_b_text.document_id as doc_id_b,
            dm_b_text.latest as doc_b_latest,
            dm_b_text.revision_number as doc_b_revision_number,
            dm_b_text.pk as doc_b_pk,
            {document_graph_relationship_definition_id} as document_graph_relationship_definition_id,
            jsonb_build_object('cited_in',dm_b_title.data) as relationship_properties
        from public_api.document_metadata dm_a_title
        inner join public_api.document_metadata dm_b_text on websearch_to_tsquery(dm_a_title.data) @@ dm_b_text.tsvec
        inner join public_api.document_metadata dm_b_title on dm_b_text.document_id = dm_b_title.document_id
        where dm_a_title.document_metadata_definition_id = {document_metadata_definition_id_a}
        and dm_b_text.document_metadata_definition_id = {document_metadata_definition_id_b}
        and dm_b_title.document_metadata_definition_id = {document_metadata_definition_id_a}
        and dm_a_title.document_id != dm_b_text.document_id
    $q$
);


insert into public_api.document_graph_relationship_definition (
    name,
    document_metadata_definition_id_a,
    document_metadata_definition_id_b,
    query_template,
    can_be_stale
)
values (
    'guidance_references_legislation',
    (select id from public_api.document_metadata_definition where name = 'legislation_identification'),
    (select id from public_api.document_metadata_definition where name = 'orpml_legislation_link'),
    $q$
        select guidance_link.document_id as doc_id_a,
            guidance_link.latest as doc_a_latest,
            guidance_link.revision_number as doc_a_revision_number,
            guidance_link.pk as doc_a_pk,
            legislation_id.document_id as doc_id_b,
            legislation_id.latest as doc_b_latest,
            legislation_id.revision_number as doc_b_revision_number,
            legislation_id.pk as doc_b_pk,
            {document_graph_relationship_definition_id} as document_graph_relationship_definition_id,
            jsonb_build_object('guidance_references_legislation',legislation_id.data) as relationship_properties
        from public_api.document_metadata legislation_id
        inner join public_api.document_metadata guidance_link on regexp_replace(guidance_link.data,'http://','https://') like regexp_replace(legislation_id.data,'http://','https://') || '%'
        where legislation_id.document_metadata_definition_id = {document_metadata_definition_id_a}
        and guidance_link.document_metadata_definition_id = {document_metadata_definition_id_b}
    $q$,
    true
);


-- insert into public_api.document_graph_relationship_definition (
--     name,
--     document_metadata_definition_id_a,
--     document_metadata_definition_id_b,
--     document_metadata_definition_index_b,
--     query_template
-- )
-- values (
--     'legislation_cited_in',
--     (select id from public_api.document_metadata_definition where name = 'title'),
--     (select id from public_api.document_metadata_definition where name = 'legislation_raw_tsvector'),
--     $i$ using gin((data::tsvector)) $i$,
--     $q$
--         select dm_a_title.document_id as doc_id_a,
--             dm_b_text.document_id as doc_id_b,
--             {document_graph_relationship_definition_id} as document_graph_relationship_definition_id,
--             jsonb_build_object('cited_in',dm_b_title.data) as relationship_properties
--         from public_api.document_metadata dm_a_title
--         inner join public_api.document_metadata dm_b_text on websearch_to_tsquery(dm_a_title.data) @@ dm_b_text.data::tsvector
--         inner join public_api.document_metadata dm_b_title on dm_b_text.document_id = dm_b_title.document_id
--         where dm_a_title.document_metadata_definition_id = {document_metadata_definition_id_a}
--         and dm_b_text.document_metadata_definition_id = {document_metadata_definition_id_b}
--         and dm_b_title.document_metadata_definition_id = {document_metadata_definition_id_a}
--         and dm_a_title.document_id != dm_b_text.document_id
--     $q$
-- );

select update_document_graph_relationship_definition((select id from public_api.document_graph_relationship_definition where name = 'legislation_cited_in'));
select update_document_graph_relationship_definition((select id from public_api.document_graph_relationship_definition where name = 'guidance_references_legislation'));