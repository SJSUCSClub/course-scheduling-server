from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import requests
import json
from django.contrib.auth.models import User
from django.contrib.auth import login
import google_auth_oauthlib.flow
from django.http import JsonResponse
import os
import time
from datetime import timezone

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['openid','https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile']


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

#add user to db
#send and create ID token from backend containing user's profile pic,name, etc httponly false so browser can access it
def GoogleAuthorize(request):
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
  authorization_url, state = flow.authorization_url(
  access_type='offline',
  include_granted_scopes='true')
  request.session['state'] = state
  return redirect(authorization_url)

def oauth2callback(request):
  state = request.session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
  authorization_response = request.build_absolute_uri()
  flow.fetch_token(authorization_response=authorization_response)
  credentials = flow.credentials
  request.session['credentials'] = credentials_to_dict(credentials)

  url = 'https://www.googleapis.com/oauth2/v2/userinfo'
  headers = {
    'Authorization': f'Bearer {credentials.token}',
    'Content-Type': 'application/json' 
  }
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    return JsonResponse({'error': 'Failed to get user info'}, status=response.status_code)

  user_info = response.json()
  email = user_info.get('email')
  first_name = user_info.get('given_name')
  last_name = user_info.get('family_name')
  if not email.endswith("@sjsu.edu"):
    return JsonResponse({'error': 'Unauthorized email address'}, status=403)
  
  user, created = User.objects.get_or_create(
    email=email,
    defaults={'username': email, 'first_name': first_name, 'last_name': last_name}
  )
  if created:
    #unusuable password bc we're using oauth
    user.set_unusable_password()
    user.save()

  user_data = {
    'email': email,
    'first_name': first_name,
    'last_name': last_name
  }
  expires_in = credentials.expiry
  
  #time since epoch
  expires_in_unix = expires_in.replace(tzinfo=timezone.utc).timestamp()

  login(request, user, backend='django.contrib.auth.backends.ModelBackend')
  response = HttpResponse('blah')
  
  response.set_cookie('idtoken',credentials.id_token, httponly=True)
  response.set_cookie('access_token', credentials.token, httponly=True)
  response.set_cookie('refresh_token', credentials.refresh_token, httponly=True)
  response.set_cookie('user_data', json.dumps(user_data))
  response.set_cookie('token_expiration', expires_in_unix)
  response['Location'] = 'http://localhost:3000'
  response.status_code = 302
  return response

def RefreshToken(request):
  header = request.headers.get('Authorization')
  if not header or not header.startswith('Bearer '):
    return JsonResponse({'error': 'Authorization header is required'}, status=404)
  
  refresh_token = header.split(' ')[1]
  
  token_url = "https://oauth2.googleapis.com/token"
  payload = {
    'client_id': os.getenv('GOOGLE_CLIENT_ID'),
    'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token'
  }
  
  response = requests.post(token_url, data=payload)
  
  if response.status_code != 200:
    return JsonResponse({'error': 'Failed to refresh token'}, status=response.status_code)
  
  response_data = response.json()
  
  new_access_token = response_data.get('access_token')
  new_id_token = response_data.get('id_token')
  expires_in = time.time()+response_data.get('expires_in')

  response = HttpResponse("blah")
  response.set_cookie('idtoken',  new_id_token, httponly=True)
  response.set_cookie('token', new_access_token, httponly=True)
  response.set_cookie('token_expiration', expires_in)
  response.status_code = 302
  return response