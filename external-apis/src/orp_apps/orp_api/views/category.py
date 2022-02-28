"""Category views."""

# Third Party

from ..constants import CATEGORY_FILTER
from ..serializers import CategorySerializer
from .mixins import ListAPIBackend, RetrieveAPIBackend


class CategoryListView(ListAPIBackend):
    """List view for categories."""

    serializer_class = CategorySerializer
    endpoint = 'distinct_document_metadata_document'
    query_params = CATEGORY_FILTER
    order_by = 'id'
    default_return = [
        {
            'category_id': 1,
            'name': 'Sample category 1'
        },
        {
            'category_id': 2,
            'name': 'Sample category 2'
        },
        {
            'category_id': 3,
            'name': 'Sample category 3'
        }
    ]


class CategoryDetailView(RetrieveAPIBackend):
    """Detail view for category."""

    serializer_class = CategorySerializer
    lookup_field = 'id'
