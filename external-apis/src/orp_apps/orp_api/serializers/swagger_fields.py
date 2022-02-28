# Third Party
from drf_yasg import openapi
from rest_framework import serializers


class DocumentTypeField(serializers.JSONField):
    """Subclass json field to display swagger schema."""

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'id': openapi.Schema(
                    title='id',
                    type=openapi.TYPE_INTEGER,
                    example=1
                ),
                'name': openapi.Schema(
                    title='name',
                    type=openapi.TYPE_STRING,
                    example='legislation.gov.uk'
                ),
            }
        }


class DocumentMetadataField(serializers.ListField):
    """Subclass list field to display swagger schema."""

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_ARRAY,
            'items': {
                'type': openapi.TYPE_OBJECT,
                'properties': {
                    'id': openapi.Schema(
                        title='id',
                        type=openapi.TYPE_INTEGER,
                        example=1
                    ),
                    'data': openapi.Schema(
                        title='data',
                        type=openapi.TYPE_STRING,
                        example='sheriff court'
                    ),
                    'name': openapi.Schema(
                        title='name',
                        type=openapi.TYPE_STRING,
                        example='legislation_named_entities'
                    ),
                    'document_metadata_definition_id': openapi.Schema(
                        title='document_metadata_definition_id',
                        type=openapi.TYPE_INTEGER,
                        example=7
                    ),
                    'distinct_metadata_id': openapi.Schema(
                        title='id',
                        type=openapi.TYPE_INTEGER,
                        example=1
                    ),
                    'url': openapi.Schema(
                        title='name',
                        type=openapi.TYPE_STRING,
                        example='http://localhost:8000/api/1.0/entities/1/'
                    ),
                }
            }
        }


class RelatedDocumentField(serializers.ListField):
    """Subclass list field to display swagger schema."""

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_ARRAY,
            'items': {
                'type': openapi.TYPE_OBJECT,
                'properties': {
                    'document_id_b': openapi.Schema(
                        title='document_id_b',
                        type=openapi.TYPE_INTEGER,
                        example=2
                    ),
                    'relationship_properties': openapi.Schema(
                        title='relationship_properties',
                        type=openapi.TYPE_OBJECT,
                        example={'cited_in': 'Generic Act title'}
                    ),
                    'url': openapi.Schema(
                        title='name',
                        type=openapi.TYPE_STRING,
                        example='http://localhost:8000/api/1.0/documents/2/'
                    ),
                }
            }
        }
