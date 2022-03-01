# Standard
import json
import logging
from typing import List, Tuple
from urllib.parse import urljoin

# Third Party
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from requests import Session
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response as RestResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)

from ..exceptions import JWTExpiredException
from ..utils import create_session, response_schema_dict

LOG = logging.getLogger(__name__)


def get_api_backend(**kwargs) -> 'ApiQueryMixin':
    """Return ApiQueryMixin object."""
    request: Request = kwargs.get('request')
    session = create_session()
    query_params = kwargs.get('query_params', {})
    for key, value in dict(request.query_params).items():
        query_params[key] = value[0]
    session.headers = {
        'Authorization': request.headers.get(
            'Authorization',
            ' '.join(('Bearer', request.session.get('jwt_token', '')))
        ),
        'Content-Type': request.headers.get('Content-Type', 'application/json'),
        'Accept': request.headers.get('Accept', 'application/json')
    }
    if 'Prefer' in request.headers:
        session.headers['Prefer'] = request.headers['Prefer']
    return ApiQueryMixin(session, query_params, request)


class ApiQueryMixin:
    """Mixin to query from API."""

    def __init__(self, session: Session, query_params: dict, request: Request):
        self.session: Session = session
        self.query_params: dict = query_params
        self.request: Request = request
        self.order_by = 'id'

    @staticmethod
    def assemble_endpoint(endpoint: str) -> str:
        """Return an endpoint with the full url."""
        endpoint = f"{endpoint.rstrip('/')}"
        return urljoin(settings.API_URL, endpoint)

    def post(self, url: str, **kwargs) -> RestResponse:
        """Make get request to API to return data."""
        LOG.info('Making POST request to %s %s', url, kwargs.get('data', {}))
        return self.session.post(url, **kwargs)

    def get(self, url: str, **kwargs) -> RestResponse:
        """Make get request to API to return data."""
        LOG.info('Making GET request to %s %s', url, kwargs.get('params', {}))
        return self.session.get(url, **kwargs)

    def sort_results(self, results: List) -> List[dict]:
        """Sort list of results by id or document_id values."""
        try:
            return sorted(results, key=lambda x: x[self.order_by])
        except KeyError as e:
            LOG.exception(e.args)
            return results

    def update_query_params(self) -> dict:
        """Render query params as a string."""
        filter_params: dict = self.query_params
        query_params_dict = dict(self.request.query_params).copy()
        for key in ('page', 'page_size'):
            if key in query_params_dict:
                query_params_dict.pop(key)
        for key, value in query_params_dict.items():
            value = value[0]
            if key != 'select':
                value = f'eq.{value}'
            filter_params.update({key: value})
        return filter_params

    @staticmethod
    def update_response_code(status_code: int, data: list) -> Tuple[int, list]:
        """Update status code based on data content."""
        if not data:
            return HTTP_404_NOT_FOUND, {} # noqa
        if data == {'message': 'JWT expired'}:
            return HTTP_401_UNAUTHORIZED, data
        return status_code, data

    def retrieve(self, **kwargs) -> Tuple:
        """Overwrite retrieve method to POST to API."""
        response = self.get(
            url=self.assemble_endpoint(kwargs.get('partial_url')),
            params=self.update_query_params(),
            headers=self.session.headers
        )
        return self.update_response_code(response.status_code, response.json())

    def list(self, **kwargs) -> Tuple[int, list]:
        """Overwrite list method to POST to API."""
        self.order_by = kwargs.get('order_by', self.order_by)
        response = self.get(
            url=self.assemble_endpoint(kwargs.get('endpoint')),
            params=self.update_query_params(),
            headers=self.session.headers
        )
        status_code, data = self.update_response_code(response.status_code, response.json())
        if status_code == HTTP_200_OK:
            return status_code, self.sort_results(data)
        data = [data]
        data.extend(kwargs['default_return'])
        return status_code, data


class RetrieveAPIBackend(RetrieveAPIView, ApiQueryMixin):
    """Mixin class to overwrite retrieve method to use api backend post."""

    http_method_names = ['get']

    def get_partial_url(self, request: Request, **kwargs) -> str:
        """Return url to query."""
        return self.endpoint

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, *args, **kwargs) -> RestResponse:
        """Call retrieve method in api backend to make post request."""
        api_backend = get_api_backend(request=request, query_params=self.query_params.copy())
        try:
            partial_url = self.get_partial_url(request, api_backend=api_backend, **kwargs)
        except ValueError as e:
            return RestResponse(status=HTTP_400_BAD_REQUEST, data=e.args)
        except JWTExpiredException as e:
            return RestResponse(status=HTTP_401_UNAUTHORIZED, data=e.args)
        status_code, instance = api_backend.retrieve(partial_url=partial_url)
        if status_code == HTTP_200_OK:
            return RestResponse(
                status=status_code,
                data=self.get_serializer(instance=instance[0]).data
            )
        return RestResponse(status=status_code, data=instance)


class ListAPIBackend(ListAPIView, ApiQueryMixin):
    """Mixin class to overwrite list method to use api backend post."""

    http_method_names = ['get']

    def get_partial_url(self, request: Request, **kwargs) -> str:
        """Return url to query."""
        return self.endpoint

    @swagger_auto_schema(responses=response_schema_dict)
    def get(self, request, *args, **kwargs) -> RestResponse:
        """Call list method in api backend to make post request."""
        api_backend = get_api_backend(request=request, query_params=self.query_params.copy())
        try:
            partial_url = self.get_partial_url(request, api_backend=api_backend, **kwargs)
        except ValueError as e:
            default_return = getattr(self, 'default_return', [])
            default_return.extend(e.args)
            return RestResponse(status=HTTP_400_BAD_REQUEST, data=default_return)
        except JWTExpiredException as e:
            return RestResponse(status=HTTP_401_UNAUTHORIZED, data=e.args)
        status_code, queryset = api_backend.list(
            endpoint=partial_url,
            order_by=self.order_by,
            default_return=getattr(self, 'default_return', [])
        )
        page = self.paginate_queryset(queryset)
        if page is not None and status_code == HTTP_200_OK:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return RestResponse(status=status_code, data=self.get_serializer(queryset, many=True).data)


class PostAPIMixin(CreateAPIView, ApiQueryMixin):
    """Mixin class to overwrite create method to use api backend post."""

    http_method_names = ['post']

    def get_partial_url(self, request: Request, **kwargs) -> str:
        """Return url to query."""
        return self.endpoint

    def handle_response(self, response: RestResponse, **kwargs) -> RestResponse:
        """Return serialized results."""
        return RestResponse(
            status=response.status_code,
            data=self.serializer_class(response.json()).data
        )

    @staticmethod
    def prepare_data(data: dict, **kwargs) -> dict:
        """Return request data.

        Should be overwritten by other classes as needed.
        """
        return data

    def post(self, request, *args, **kwargs) -> RestResponse:
        """Call list method in api backend to make post request."""
        api_backend = get_api_backend(request=request, query_params=self.query_params.copy())
        try:
            partial_url = self.get_partial_url(request, api_backend=api_backend, **kwargs)
        except ValueError as e:
            default_return = getattr(self, 'default_return', [])
            default_return.extend(e.args)
            return RestResponse(status=HTTP_400_BAD_REQUEST, data=default_return)
        except JWTExpiredException as e:
            return RestResponse(status=HTTP_401_UNAUTHORIZED, data=e.args)
        missing_keys = set(request.data.keys()).difference(self.expected_keys)
        if missing_keys:
            return RestResponse(
                status=HTTP_400_BAD_REQUEST,
                data={'message': f'Missing keys from input {",".join(list(missing_keys))}'}
            )
        data = json.dumps(self.prepare_data(dict(request.data), api_backend=api_backend, **kwargs))
        return self.handle_response(
            api_backend.post(
                url=api_backend.assemble_endpoint(partial_url),
                data=data,
                headers=api_backend.session.headers
            ),
            api_backend=api_backend
        )
