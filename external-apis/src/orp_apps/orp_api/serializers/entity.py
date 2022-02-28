"""Entity serializer."""

# Third Party
from rest_framework import serializers

from .mixins import LinkedListSerializer, LinkedSerializer


class EntityListSerializer(LinkedListSerializer):
    """Serializer for Entity list."""

    class Meta:
        """Meta class definition."""

        hyperlink_list: tuple = (
            ('url', 'entity-detail'),
            ('documents', 'entity-documents')
        )
        hyperlink_keys: tuple = ('id',)


class EntitySerializer(LinkedSerializer):
    """Detailed serializer for Entity."""

    id = serializers.IntegerField(read_only=True)
    data = serializers.CharField(read_only=True)
    document_metadata_definition_id = serializers.IntegerField(read_only=True)
    tsvec = serializers.CharField(read_only=True)
    _hash = serializers.CharField(read_only=True)

    class Meta:
        """Meta class definition."""

        list_serializer_class = EntityListSerializer
        hyperlink_list: tuple = (
            ('documents', 'entity-documents'),
        )
        hyperlink_keys: tuple = ('id',)
