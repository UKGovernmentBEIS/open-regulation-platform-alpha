"""Views to manage subscriptions."""

# Third Party
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

# Project
from orp_apps.orp_api.serializers import GenericSerializer
from orp_apps.orp_api.views.mixins import ListAPIBackend, PostAPIMixin


class SubscriptionEventTypesView(ListAPIBackend):
    """View to list all subscription event types."""

    endpoint = 'event_type'
    order_by = 'id'
    query_params = {}
    serializer_class = GenericSerializer


class RevisionSubscriptionView(PostAPIMixin, ListAPIBackend):
    """View to list and create subscriptions to document revisions."""

    endpoint = 'event_subscription'
    order_by = 'id'
    query_params = {}
    serializer_class = GenericSerializer
    http_method_names = ['get', 'post']
    expected_keys = {'event_filters', 'event_type_id', 'deliver_async'}

    def get_document(self, **kwargs) -> list:
        """Return data for related document."""
        api_backend = kwargs.get('api_backend')
        response = api_backend.get(
            self.assemble_endpoint('document'),
            params={'id': f'eq.{kwargs.get("id")}'}
        )
        return response.json()

    def get_event_type(self, **kwargs) -> list:
        """Return data for related event type."""
        api_backend = kwargs.get('api_backend')
        response = api_backend.get(
            self.assemble_endpoint('event_type'),
            params={'event_name': f'eq.{kwargs.get("event_type")}'}
        )
        return response.json()

    def prepare_data(self, data: dict, **kwargs) -> dict:
        """Generate data object from related document and event type data."""
        if data:
            return data
        document = self.get_document(**kwargs)[0]
        event_type = self.get_event_type(**kwargs)[0]
        data = {
            'event_type_id': event_type['id'],
            'event_filters': [{'event_key':  document['pk'], 'event_filter': document['pk']}],
            'deliver_async': event_type['can_async']
        }
        return data

    def handle_response(self, response: Response, **kwargs) -> Response:
        """Return serialized results."""
        many = False
        if response.status_code in (HTTP_200_OK, HTTP_201_CREATED):
            api_backend = kwargs.get('api_backend')
            response = api_backend.get(self.assemble_endpoint(self.endpoint))
            many = True
        return Response(
            status=response.status_code,
            data=self.serializer_class(response.json(), many=many).data
        )
