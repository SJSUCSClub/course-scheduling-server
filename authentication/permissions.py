from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, NotFound
from authentication.exceptions import InternalServerError
import requests
User = get_user_model()

class GooglePermission(BasePermission):
    def authorization(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            raise NotAuthenticated('No access token')
        try:
            response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}')
            if response.status_code != 200:
                raise NotAuthenticated("Invalid access token")
            token_info = response.json()
            email = token_info.get('email')

            if not email:
                raise InternalServerError()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise NotFound('User not found')
            
            #as long as it returns a valid user object, they're authorized
            return (user, None)
        except:
            raise InternalServerError()