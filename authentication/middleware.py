import requests
import time
from django.conf import settings
from django.http import JsonResponse
from authentication.utils.refreshToken import refresh

class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        #only user endpoints will refresh tokens when accessed
        if not request.path.startswith("/core/users/"):
            return self.get_response(request)
        access_token = request.COOKIES.get('access_token')
        if access_token:
            response = self.get_token_info(request,access_token)
            if not response:
                refresh_token = request.COOKIES.get('refresh_token')
                if not refresh_token:
                    return JsonResponse({'error': 'No refresh token'}, status=401)
                response_data = refresh(refresh_token)
                if response_data == None:
                    return JsonResponse({'error': 'Invalid access and refresh token'}, status=401)

                new_access_token = response_data.get('access_token')
                new_id_token = response_data.get('id_token')
                expires_in = time.time()+response_data.get('expires_in')
                
                self.get_token_info(request,new_access_token)

                response = self.get_response(request)
                response.set_cookie('idtoken',  new_id_token, httponly=True)
                response.set_cookie('access_token', new_access_token, httponly=True)
                response.set_cookie('token_expiration', expires_in)
                return response
        return self.get_response(request)
    def get_token_info(self, request, access_token):
        try:
            response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}')
            if response.status_code == 200:
                response = response.json()
                request.token_res = response
                return response
            return None
        except:
            print(f"Error fetching token info: {e}")
            return None