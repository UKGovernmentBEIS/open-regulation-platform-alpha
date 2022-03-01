# Third Party
from rest_framework.relations import Hyperlink
from rest_framework.reverse import reverse
from rest_framework.serializers import ListSerializer, Serializer


class BaseLinkedSerializer:

    def add_hyperlinks(self, result, **kwargs):
        """Insert hyperlinks into serializer data."""
        request = self.context.get('request')
        for key, url_name in self.Meta.hyperlink_list:
            result[key] = Hyperlink(
                reverse(url_name, kwargs=kwargs.get('data'), request=request),
                kwargs.get('key')
            )
        return result


class LinkedSerializer(BaseLinkedSerializer, Serializer):

    def to_representation(self, instance):
        content = super().to_representation(instance)
        content.update(instance)
        request = self.context.get('request')
        try:
            key = next((key for key in self.Meta.hyperlink_keys if key in content))
        except StopIteration:
            pass
        else:
            id_value = content.get(key)
            if id_value:
                self.add_hyperlinks(
                    content,
                    key=id_value,
                    data={'id': id_value, 'version': request.version}
                )
        return content


class LinkedListSerializer(BaseLinkedSerializer, ListSerializer):
    """Serializer class to add hyperlinks to list of results."""

    def to_representation(self, instance):
        """Add hyperlinks to related assets."""
        content = super().to_representation(instance)
        request = self.context.get('request', None)
        if request:
            for result in content:
                try:
                    key = next((key for key in self.Meta.hyperlink_keys if key in result))
                except StopIteration:
                    pass
                else:
                    id_value = result.get(key)
                    if id_value:
                        self.add_hyperlinks(
                            result,
                            key=id_value,
                            data={'id': id_value, 'version': request.version}
                        )
        return content
