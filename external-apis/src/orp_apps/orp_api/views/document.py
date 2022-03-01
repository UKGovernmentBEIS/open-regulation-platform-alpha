"""Document views."""

from ..constants import DOCUMENT_DETAIL_PARAMS, DOCUMENT_FILTER_PARAMS
from ..serializers import DocumentSerializer
from .mixins import ListAPIBackend, RetrieveAPIBackend


class DocumentListView(ListAPIBackend):
    """List view for Documents with outstanding feedback."""

    serializer_class = DocumentSerializer
    endpoint = 'document'
    query_params = DOCUMENT_FILTER_PARAMS
    order_by = 'document_id'


class DocumentListSearchView(DocumentListView):
    """List view to display Documents returned from search."""

    def get_partial_url(self, request, **kwargs):
        """Add filter to return multiple documents."""
        return self.endpoint + f'?id=in.({kwargs["id_list"]})'


class DocumentOutstandingFeedbackList(DocumentListView):
    """List view for Documents with outstanding feedback."""

    endpoint = 'docs_with_outstanding_feedback'


class DocumentCompletedFeedbackList(DocumentListView):
    """List view for Documents with completed feedback."""

    endpoint = 'docs_with_completed_feedback'


class DocumentDetailView(RetrieveAPIBackend):
    """Detail view for Document."""

    serializer_class = DocumentSerializer
    endpoint = 'document'
    query_params = DOCUMENT_DETAIL_PARAMS

    def get_partial_url(self, request, **kwargs):
        """Add filter to return single document."""
        return self.endpoint + f'?id=eq.{kwargs["id"]}'
