"""Taxonomy views."""

from ..constants import CLASSIFICATION_FILTER_FOR_ID, TAXONOMY_FITTER
from ..serializers import TaxonomySerializer
from ..utils.utils import make_get_request
from .mixins import ListAPIBackend, RetrieveAPIBackend


class TaxonomyListView(ListAPIBackend):
    """List view for taxonomies."""

    serializer_class = TaxonomySerializer
    query_params = TAXONOMY_FITTER
    endpoint = 'distinct_document_metadata'
    order_by = 'id'
    default_return = [
        {
            'id': 1,
            'name': 'Sample taxonomy 1'
        },
        {
            'id': 2,
            'name': 'Sample taxonomy 2'
        },
        {
            'id': 3,
            'name': 'Sample taxonomy 3'
        }
    ]

    def get_partial_url(self, request, **kwargs) -> str:
        """Query to get id for classifications and use it to generate partial url."""
        return make_get_request(
            api_backend=kwargs.get('api_backend'),
            url=self.assemble_endpoint('document_metadata_definition'),
            endpoint=self.endpoint,
            primary_filter='?document_metadata_definition_id=eq.{}',
            secondary_filter=CLASSIFICATION_FILTER_FOR_ID
        )


class TaxonomyDetailView(RetrieveAPIBackend):
    """Detail view for taxonomy."""

    serializer_class = TaxonomySerializer
    lookup_field = 'id'
    endpoint = 'distinct_document_metadata'
    query_params = {}

    def get_partial_url(self, request, **kwargs):
        """Query to get id for classifications and use it to generate partial url."""
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
            secondary_filter=CLASSIFICATION_FILTER_FOR_ID
        )
