"""Django views."""

# Standard
from collections import OrderedDict

# Third Party
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIRoot(APIView):
    """Return a root api view (browseable)."""

    def get(self, request, *args, **kwargs):
        """List of browseable API endpoints."""
        return Response(
            OrderedDict(
                (
                    ('api-taxonomies', reverse('taxonomy-list', request=request)),
                    ('api-documents', reverse('document-list', request=request)),
                    (
                        'api-documents-with-outstanding-feedback',
                        reverse('document-outstanding-feedback-list', request=request)
                    ),
                    (
                        'api-documents-with-completed-feedback',
                        reverse('document-completed-feedback-list', request=request)
                    ),
                    ('api-entities', reverse('entity-list', request=request)),
                    ('api-document-search', reverse('search-documents', request=request)),
                    ('api-search-graph', reverse('graph-documents', request=request)),
                    ('subscription-event-list', reverse('subscription-event-list', request=request)),
                )
            )
        )
