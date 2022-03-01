"""Category serializer."""

# Standard
from collections import OrderedDict

# Third Party
from rest_framework.serializers import Serializer

from .mixins import LinkedListSerializer


class CategoryListSerializer(LinkedListSerializer):
    """Serializer for category list."""

    class Meta:
        """Meta class definition."""

        hyperlink_list: tuple = (('url', 'category-detail'),)

    def to_representation(self, instance):
        """Add hyperlinks to related assets."""
        content = [OrderedDict(result) for result in instance]
        request = self.context.get('request', None)
        kwargs = self.context['view'].kwargs
        if request:
            for result in content:
                if 'id' in result:
                    id_value = result.get('id')
                    data = kwargs.copy()
                    data['category_id'] = id_value
                    self.add_hyperlinks(result, key=id_value, data=data)
        return content


class CategorySerializer(Serializer):
    """Detailed serialized for categories."""

    def to_representation(self, instance):
        content = super().to_representation(instance)
        content.update(instance)
        return content

    class Meta:
        """Meta class definition."""

        list_serializer_class = CategoryListSerializer
