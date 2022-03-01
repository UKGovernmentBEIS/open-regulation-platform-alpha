"""Login view."""

# Standard
import logging
from urllib.parse import urljoin

# Third Party
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_302_FOUND,
    HTTP_400_BAD_REQUEST
)
from rest_framework.views import APIView

LOG = logging.getLogger(__name__)


class LoginView(APIView):
    """Subclass login view to add jwt to cookies."""

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Return jwt token or render next screen based on http content type."""
        if 'email' not in request.data or 'password' not in request.data:
            return JsonResponse({'error': 'Values for "email" and "password" required".'})
        response = requests.post(
            url=urljoin(settings.API_URL, 'rpc/login'),
            data={'email': request.data.get('email'), 'password': request.data.get('password')}
        )
        if response.status_code in (HTTP_200_OK, HTTP_302_FOUND):
            token = response.json()['signed_jwt']
            request.session['jwt_token'] = token
            return JsonResponse(status=response.status_code, data={'signed_jwt': token})
        return JsonResponse(status=HTTP_400_BAD_REQUEST, data=response.json())
