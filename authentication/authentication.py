from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
import os 
import requests
User = get_user_model()

class GoogleIDTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            raise exceptions.AuthenticationFailed('No access token in cookies')
        try:
            response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}')
            if response.status_code != 200:
                raise exceptions.AuthenticationFailed('Invalid token')
            token_info = response.json()
            email = token_info.get('email')

            if not email:
                raise exceptions.AuthenticationFailed('Token did not contain email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
            
            #as long as it returns a valid user object, they're authorized
            return (user, None)
        except:
            raise exceptions.AuthenticationFailed('Invalid token')