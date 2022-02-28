"""Document serializer."""

# Third Party
from rest_framework import serializers
from rest_framework.relations import Hyperlink
from rest_framework.reverse import reverse

from ..constants import RELATED_DOCUMENT_MAP
from .mixins import LinkedListSerializer, LinkedSerializer
from .swagger_fields import (
    DocumentMetadataField,
    DocumentTypeField,
    RelatedDocumentField
)


class DocumentListSerializer(LinkedListSerializer):
    """Serializer for Document list."""

    class Meta:
        """Meta class definition."""

        hyperlink_list: tuple = (
            ('url', 'document-detail'),
        )
        hyperlink_keys: tuple = ('document_id', 'id')


class DocumentSerializer(LinkedSerializer):
    """Detailed serializer for Documents."""

    document_id = serializers.IntegerField(read_only=True)
    document_type = DocumentTypeField(read_only=True)
    document_metadata = DocumentMetadataField(read_only=True)
    related_documents = RelatedDocumentField(read_only=True)
    reverse_related_documents = RelatedDocumentField(read_only=True)
    entities = DocumentMetadataField(read_only=True)
    raw_text = serializers.CharField(read_only=True)
    document_enrichments = serializers.ListField(read_only=True)

    class Meta:
        """Meta class definition."""

        list_serializer_class = DocumentListSerializer
        hyperlink_list: tuple = ()
        hyperlink_keys: tuple = ()

    def to_representation(self, instance):
        """Insert links to related documents."""
        content = super().to_representation(instance=instance)
        if not instance:
            return content
        request = self.context.get('request')
        for field_name, id_key in RELATED_DOCUMENT_MAP.items():
            if field_name in content:
                for related_document in content[field_name]:
                    id_value = related_document.get(id_key)
                    related_document['url'] = Hyperlink(
                        reverse(
                            'document-detail',
                            kwargs={'id': id_value, 'version': request.version},
                            request=request
                        ),
                        id_value
                    )
        content['entities'] = []
        if 'document_id' in content:
            id_value = content['document_id']
            content['new_document_revision'] = Hyperlink(
                reverse(
                    'document-detail-subscriptions',
                    kwargs={
                        'id': id_value,
                        'version': request.version,
                        'event_type': 'new_document_revision'
                    },
                    request=request
                ),
                id_value
            )
        if 'document_metadata' in content:
            for metadata in content['document_metadata']:
                id_value = metadata.get('distinct_metadata_id')
                metadata_type = metadata.get('name')
                url = None
                is_entity = metadata_type == 'legislation_named_entities'
                if is_entity:
                    url = 'entity-detail'
                elif metadata_type == 'classification':
                    url = 'taxonomy-detail'
                if id_value and url:
                    metadata['url'] = Hyperlink(
                        reverse(
                            url,
                            kwargs={'id': id_value, 'version': request.version},
                            request=request
                        ),
                        id_value
                    )

                if is_entity:
                    content['entities'].append(metadata)
        if 'raw_text' in content and content['raw_text'] == '<akomaNtoso/>':
            del content['raw_text']
        return content


class SearchListSerializer(LinkedListSerializer):
    """Serializer for Document list."""

    class Meta:
        """Meta class definition."""

        hyperlink_list: tuple = (
            ('url', 'document-detail'),
        )
        hyperlink_keys: tuple = ('document_id', 'id')


class SearchSerializer(LinkedSerializer):

    class Meta:
        """Meta class definition."""

        list_serializer_class = SearchListSerializer
        hyperlink_list: tuple = ()
        hyperlink_keys: tuple = ()
