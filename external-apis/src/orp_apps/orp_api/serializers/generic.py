"""Generic serializer classes."""

# Third Party
from rest_framework.serializers import ListSerializer, Serializer


class GenericListSerializer(ListSerializer):
    """Serializer for category list."""

    class Meta:
        """Meta class definition."""

        hyperlink_list: tuple = ()


class GenericSerializer(Serializer):
    """Detailed serialized for categories."""

    def to_representation(self, instance):
        content = super().to_representation(instance)
        content.update(instance)
        return content

    class Meta:
        """Meta class definition."""

        list_serializer_class = GenericListSerializer
