"""Entity views."""

from ..constants import ENTITY_FILTER, ENTITY_FILTER_FOR_ID
from ..serializers import EntitySerializer
from ..utils.utils import make_get_request
from .mixins import ListAPIBackend, RetrieveAPIBackend


class EntityListView(ListAPIBackend):
    """List view for Named Entity."""

    serializer_class = EntitySerializer
    query_params = ENTITY_FILTER
    endpoint = 'distinct_document_metadata'
    order_by = 'id'
    default_return = [
        {
            'id': 1,
            'name': 'Sample entity 1'
        },
        {
            'id': 2,
            'name': 'Sample entity 2'
        },
        {
            'id': 3,
            'name': 'Sample entity 3'
        }
    ]

    def get_partial_url(self, request, **kwargs):
        """Query to get id for named entities and use it to generate partial url."""
        return make_get_request(
            api_backend=kwargs.get('api_backend'),
            url=self.assemble_endpoint('document_metadata_definition'),
            endpoint=self.endpoint,
            primary_filter='?document_metadata_definition_id=eq.{}',
            secondary_filter=ENTITY_FILTER_FOR_ID
        )


class EntityDetailView(RetrieveAPIBackend):
    """Detail view for Named Entity."""

    serializer_class = EntitySerializer
    lookup_field = 'id'
    endpoint = 'distinct_document_metadata'
    query_params = {}

    def get_partial_url(self, request, **kwargs):
        """Query to get id for named entities and use it to generate partial url."""
        return make_get_request(
            api_backend=kwargs.get('api_backend'),
            url=self.assemble_endpoint('document_metadata_definition'),
            endpoint=self.endpoint,
            primary_filter='&'.join(
                (
                    '?document_metadata_definition_id=eq.{}',
                    f'id=eq.{kwargs[self.lookup_field]}'
                )
            ),
            secondary_filter=ENTITY_FILTER_FOR_ID
        )
