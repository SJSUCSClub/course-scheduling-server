from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()

class GoogleIDTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            raise exceptions.AuthenticationFailed('No Bearer token')
        
        id_token_str = header.split(' ')[1]
        try:
            id_info = id_token.verify_oauth2_token(id_token_str, requests.Request(), "699655080164-8oubieg94ai970d0ltqdcv0ff7f2ubuo.apps.googleusercontent.com")
            email = id_info.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')
            
            #as long as it returns a valid user object, they're authorized
            return (user, None)
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token')