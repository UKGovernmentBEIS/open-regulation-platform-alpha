# Third Party
from drf_yasg import openapi

response_schema_dict = {
    '400': openapi.Response(
        description='Bad Request',
        examples={
            'application/json': {
                'hint': 'string',
                'details': 'string',
                'code': 'string',
                'message': 'string',
            }
        }
    ),
    '401': openapi.Response(
        description='Not Authorized',
        examples={
            'application/json': {
                'message': 'JWT expired'
            }
        }
    ),
    '404': openapi.Response(
        description='File Not Found',
        type=openapi.TYPE_ARRAY,
        examples=['']
    )
}

search_parameters = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'filters': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items={
                'type': openapi.TYPE_OBJECT,
                'properties': {
                    'operator': openapi.Schema(
                        title='operator',
                        type=openapi.TYPE_STRING,
                        example='and'
                    ),
                    'filter_elements': openapi.Schema(
                        title='filter_elements',
                        type=openapi.TYPE_ARRAY,
                        items={
                            'type': openapi.TYPE_OBJECT,
                            'properties': {
                                'document_metadata_category': openapi.Schema(
                                    title='document_metadata_category',
                                    type=openapi.TYPE_STRING,
                                    example='title'
                                ),
                                'websearch_tsquery': openapi.Schema(
                                    title='websearch_tsquery',
                                    type=openapi.TYPE_STRING,
                                    example='asbestos'
                                ),
                            }
                        }
                    ),
                }
            }
        ),
    }
)

graph_parameters = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'filters': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items={
                'type': openapi.TYPE_OBJECT,
                'properties': {
                    'operator': openapi.Schema(
                        title='operator',
                        type=openapi.TYPE_STRING,
                        example='and'
                    ),
                    'filter_elements': openapi.Schema(
                        title='filter_elements',
                        type=openapi.TYPE_ARRAY,
                        items={
                            'type': openapi.TYPE_OBJECT,
                            'properties': {
                                'document_metadata_category': openapi.Schema(
                                    title='document_metadata_category',
                                    type=openapi.TYPE_STRING,
                                    example='title'
                                ),
                                'websearch_tsquery': openapi.Schema(
                                    title='websearch_tsquery',
                                    type=openapi.TYPE_STRING,
                                    example='asbestos'
                                ),
                            }
                        }
                    ),
                    'relationship_names': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items={
                            'type': openapi.TYPE_STRING,
                            'example': 'guidance_references_legislation'
                        }
                    ),
                    'metadata_categories': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items={
                            'type': openapi.TYPE_STRING,
                            'example': ['title', 'classification']
                        }
                    ),
                }
            }
        ),
    }
)

search_results = {
    '200': openapi.Schema(
        description='Success',
        type=openapi.TYPE_ARRAY,
        items={
            'type': openapi.TYPE_INTEGER,
            'example': [1, 2, 3]
        }
    )
}

graph_results = {
    '200': openapi.Schema(
        description='Success',
        type=openapi.TYPE_OBJECT,
        properties={
            'edges': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items={
                    'type': openapi.TYPE_OBJECT,
                    'properties': {
                        'data': openapi.Schema(
                            title='id',
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    title='id',
                                    type=openapi.TYPE_INTEGER,
                                    example=9
                                ),
                                'source': openapi.Schema(
                                    title='id',
                                    type=openapi.TYPE_INTEGER,
                                    example=117
                                ),
                                'target': openapi.Schema(
                                    title='id',
                                    type=openapi.TYPE_INTEGER,
                                    example=113
                                ),
                                'properties': openapi.Schema(
                                    title='id',
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'guidance_references_legislation': openapi.Schema(
                                            title='guidance_references_legislation',
                                            type=openapi.TYPE_STRING,
                                            example='http://www.legislation.gov.uk/id/uksi/2012/632'
                                        )
                                    }
                                ),
                                'property_key': openapi.Schema(
                                    title='property_key',
                                    type=openapi.TYPE_STRING,
                                    example='guidance_references_legislation'
                                ),
                            }
                        )
                    }
                }
            ),
            'nodes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items={
                    'type': openapi.TYPE_OBJECT,
                    'properties': {
                        'data': openapi.Schema(
                            title='id',
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    title='id',
                                    type=openapi.TYPE_INTEGER,
                                    example=113
                                ),
                                'title': openapi.Schema(
                                    title='title',
                                    type=openapi.TYPE_STRING,
                                    example='The Control of Asbestos Regulations 2012'
                                ),
                                'document_type_id': openapi.Schema(
                                    title='document_type_id',
                                    type=openapi.TYPE_INTEGER,
                                    example=1
                                ),
                                'document_type_name': openapi.Schema(
                                    title='document_type_name',
                                    type=openapi.TYPE_STRING,
                                    example='legislation.gov.uk'
                                ),
                            }
                        )
                    }
                }
            ),
        }
    )
}
graph_results.update(response_schema_dict)
search_results.update(response_schema_dict)
