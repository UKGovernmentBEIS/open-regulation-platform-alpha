
DOCUMENT_METADATA_CATEGORY = 'document_metadata_view.category'
DOCUMENT_METADATA_VIEW = 'in.(title,longtitle,enacted,identification,classification,named_entities,html)'  # noqa: E501
DOCUMENT_ID = 'document_id:id'
DOCUMENT_TYPE = 'document_type(id,name)'
DOCUMENT_PRIMARY_KEY = 'primary_key:pk'
DOCUMENT_REVISION_NUMBER = 'revision_number'
DOCUMENT_METADATA = 'document_metadata:document_metadata_view(id,data,name,document_metadata_definition_id,distinct_metadata_id)'  # noqa: E501
DOCUMENT_ENRICHMENTS = 'document_enrichments:enrichment(id,data,extent,enrichment_def(id,name,type),enrichment_feedback(good,notes,user_id))'  # noqa: E501
DOCUMENT_RAW_TEXT = 'raw_text'
DOCUMENT_RELATED = 'related_documents:document_graph!document_id_a(document_id_b,relationship_properties),reverse_related_documents:document_graph!document_id_b(document_id_a,relationship_properties)'  # noqa: E501
DOCUMENT_LATEST = 'latest'
DOCUMENT_FILTER_BOOLEAN = 'eq.true'
SELECT = 'select'

DOCUMENT_SELECT_FILTER = ','.join(
    [
        DOCUMENT_ID,
        DOCUMENT_PRIMARY_KEY,
        DOCUMENT_REVISION_NUMBER,
        DOCUMENT_METADATA,
        DOCUMENT_ENRICHMENTS,
        DOCUMENT_LATEST
    ]
)
DOCUMENT_SELECT_FILTER_DETAIL = ','.join(
    [
        DOCUMENT_ID,
        DOCUMENT_PRIMARY_KEY,
        DOCUMENT_REVISION_NUMBER,
        DOCUMENT_METADATA,
        DOCUMENT_ENRICHMENTS,
        DOCUMENT_RAW_TEXT,
        DOCUMENT_TYPE,
        DOCUMENT_RELATED,
        DOCUMENT_LATEST
    ]
)
DOCUMENT_FILTER_PARAMS = {
    SELECT: DOCUMENT_SELECT_FILTER,
    DOCUMENT_LATEST: DOCUMENT_FILTER_BOOLEAN,
    DOCUMENT_METADATA_CATEGORY: DOCUMENT_METADATA_VIEW
}
DOCUMENT_DETAIL_PARAMS = {
    SELECT: DOCUMENT_SELECT_FILTER_DETAIL,
    DOCUMENT_LATEST: DOCUMENT_FILTER_BOOLEAN,
    DOCUMENT_METADATA_CATEGORY: DOCUMENT_METADATA_VIEW
}

ENTITY_FILTER = {SELECT: 'id,data'}
TAXONOMY_FITTER = {SELECT: 'id,data'}
CATEGORY_FILTER = {SELECT: 'id,distinct_document_metadata_id,document_metadata_id'}
CLASSIFICATION_FILTER_FOR_ID = {SELECT: 'id', 'name': 'eq.legislation_classification'}
ENTITY_FILTER_FOR_ID = {SELECT: 'id', 'name': 'eq.legislation_named_entities'}

RELATED_DOCUMENT_MAP = {
    'related_documents': 'document_id_b',
    'reverse_related_documents': 'document_id_a'
}
