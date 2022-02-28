"""Taxonomy serializer."""

# Third Party
from rest_framework import serializers

from .mixins import LinkedListSerializer, LinkedSerializer


class TaxonomyListSerializer(LinkedListSerializer):
    """Serializer for Taxonomy list."""

    class Meta:
        """Meta class definition."""

        hyperlink_list: tuple = (
            ('url', 'taxonomy-detail'),
            ('categories', 'categories-list')
        )
        hyperlink_keys: tuple = ('id',)


class TaxonomySerializer(LinkedSerializer):
    """Detailed serializer for taxonomies."""

    id = serializers.IntegerField(read_only=True)
    data = serializers.CharField(read_only=True)
    document_metadata_definition_id = serializers.IntegerField(read_only=True)
    tsvec = serializers.CharField(read_only=True)
    _hash = serializers.CharField(read_only=True)

    class Meta:
        """Meta class definition."""

        list_serializer_class = TaxonomyListSerializer
        hyperlink_list: tuple = (
            ('categories', 'categories-list'),
        )
        hyperlink_keys: tuple = ('id',)
