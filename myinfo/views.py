import logging

from django.core.cache import cache
from django.utils.crypto import get_random_string
from rest_framework import generics, status, parsers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .client import MyInfoPersonalClientV4

log = logging.getLogger(__name__)
myinfo_client = MyInfoPersonalClientV4()

class MyInfoAuthorizeAPIView(generics.GenericAPIView):
    """
    Handles the authorization process by generating the SingPass authorization URL.
    """
    def get(self, request):
        callback_url = request.GET.get("callback_url")
        if not callback_url:
            raise ValidationError({"error": "callback_url is required"})

        state = get_random_string(length=16)
        # Store state in Redis cache for later validation
        cache.set(state, state, timeout=300)
        authorize_url = myinfo_client.get_authorise_url(state, callback_url)
        return Response({"authorize_url": authorize_url, "state": state}, status=status.HTTP_200_OK)

class MyInfoCallbackAPIView(generics.GenericAPIView):
    """
    Handles the callback after SingPass authorization and retrieves user data.
    """
    parser_classes = (parsers.JSONParser,)

    def get(self, request):
        """
        Handles the GET request from SingPass after authentication.
        """
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code or not state:
            return Response({"error": "Missing authorization code or state."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_data = myinfo_client.retrieve_resource(
                auth_code=code,
                state=state,
                callback_url=request.build_absolute_uri()
            )
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            log.exception(f"Error while fetching user data: {e}")
            return Response(
                {"error": "Failed to fetch user data. Please try again later."},
                status=status.HTTP_400_BAD_REQUEST
            )
