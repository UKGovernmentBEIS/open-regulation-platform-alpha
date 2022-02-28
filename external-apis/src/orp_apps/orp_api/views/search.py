# Standard
import json
from json.decoder import JSONDecodeError

# Third Party
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_302_FOUND

# Project
from orp_apps.orp_api.serializers import SearchSerializer
from orp_apps.orp_api.utils.swagger_responses import (
    graph_parameters,
    graph_results,
    search_parameters,
    search_results
)
from orp_apps.orp_api.views.mixins import PostAPIMixin
from orp_apps.orp_api.constants import DOCUMENT_FILTER_PARAMS

FILTERS_KEY = 'filters'


class DocumentSearch(PostAPIMixin):
    """View to search for documents."""

    endpoint = 'rpc/document_search'
    query_params = {}
    serializer_class = SearchSerializer
    expected_keys = {FILTERS_KEY}

    @staticmethod
    def prepare_data(data, **kwargs):
        """Update request data so that its a valid json object."""
        if isinstance(data[FILTERS_KEY][0], str):
            return {FILTERS_KEY: json.loads(data[FILTERS_KEY][0])}
        return data

    @swagger_auto_schema(request_body=search_parameters, responses=search_results)
    def post(self, request, *args, **kwargs):
        """Add swagger schema to method."""
        return super().post(request, *args, **kwargs)

    def handle_response(self, response, **kwargs):
        """Make request to document list to display all search results."""
        api_backend = kwargs.get('api_backend')
        if response.status_code in (HTTP_200_OK, HTTP_201_CREATED, HTTP_302_FOUND):
            id_list = ','.join([str(document_id) for document_id in response.json()])
            query_params = DOCUMENT_FILTER_PARAMS.copy()
            query_params['id'] = f'in.({id_list})'
            response = api_backend.get(
                self.assemble_endpoint('document'),
                params=query_params
            )
        return Response(status=response.status_code, data=response.json())


class DocumentGraphSearch(PostAPIMixin):
    """View to search for documents and return graph object."""

    endpoint = 'rpc/graph_search'
    query_params = {}
    serializer_class = SearchSerializer
    expected_keys = {FILTERS_KEY, 'relationship_names', 'metadata_categories'}

    @staticmethod
    def prepare_data(data, **kwargs):
        """Update request data so that its a valid json object."""
        for k, v in data.items():
            if isinstance(v, list) and len(v):
                try:
                    data[k] = json.loads(v[0])
                except (JSONDecodeError, TypeError):
                    pass
        return data

    @swagger_auto_schema(request_body=graph_parameters, responses=graph_results)
    def post(self, request, *args, **kwargs):
        """Add swagger schema to method."""
        return super().post(request, *args, **kwargs)
