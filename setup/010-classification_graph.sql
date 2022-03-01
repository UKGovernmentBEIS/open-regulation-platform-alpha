--
-- Copyright (C) Analytics Engines
-- 2021 Alastair McKinley (a.mckinley@analyticsengines.com)
--

insert into public_api.document_graph_relationship_definition (
    name,
    document_metadata_definition_id_a,
    document_metadata_definition_id_b,
    query_template
)
values (
    'same_classification',
    (select id from public_api.document_metadata_definition where name = 'legislation_classification'),
    (select id from public_api.document_metadata_definition where name = 'legislation_classification'),
    $q$
        select id_a as doc_id_a,
            d_a.latest as doc_a_latest,
            d_a.revision_number as doc_a_revision_number,
            d_a.pk as doc_a_pk,
            id_b as doc_id_b,
            d_b.latest as doc_b_latest,
            d_b.revision_number as doc_b_revision_number,
            d_b.pk as doc_b_pk,
            {document_graph_relationship_definition_id} as document_graph_relationship_definition_id,
            jsonb_build_object('same_classification',data) as relationship_properties
        from (
            select ddmd.distinct_document_metadata_id,
                ddm.data,
                array_agg(document_id) as document_ids
            from public_api.distinct_document_metadata_document ddmd
            inner join public_api.distinct_document_metadata ddm on ddmd.distinct_document_metadata_id = ddm.id
            inner join public_api.document_metadata dm on ddmd.document_metadata_id = dm.id
            where dm.document_metadata_definition_id = {document_metadata_definition_id_a}
            group by 1,2
            having count(*) > 1 and count(*) < 10
        ) s,
        lateral distinct_pairs(document_ids) as dp(id_a,id_b)
        inner join public_api.document d_a on d_a.id = id_a
        inner join public_api.document d_b on d_b.id = id_b
    $q$
);



select update_document_graph_relationship_definition((select id from public_api.document_graph_relationship_definition where name = 'same_classification'));