# Third Party
from rest_framework.status import HTTP_401_UNAUTHORIZED

from ..exceptions import JWTExpiredException


def make_get_request(api_backend, url: str, endpoint: str, primary_filter: str, secondary_filter: dict) -> str:
    """Make GET request to return ID value that will be used to generate URL."""
    response = api_backend.get(url, params=secondary_filter)
    data = response.json()
    if response.status_code == HTTP_401_UNAUTHORIZED:
        raise JWTExpiredException(data)
    if data:
        id_value = data[0]['id']
        return endpoint + primary_filter.format(id_value)
    raise ValueError({'message': 'No ID value can be found for metadata definition'})
