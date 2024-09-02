from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import requests
import json
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
import google_auth_oauthlib.flow
from django.http import JsonResponse
from core.sql_funcs import insert
import os
import time
from datetime import timezone
from rest_framework.decorators import api_view, permission_classes
from authentication.permissions import AuthenticatedPermission,NotAuthenticatedPermission

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
@api_view(['GET'])
@permission_classes([NotAuthenticatedPermission])
def GoogleAuthorize(request):
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
  authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
  )
  request.session['state'] = state
  return redirect(authorization_url)

@api_view(['GET'])
@permission_classes([NotAuthenticatedPermission])
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
  try:
    insert('users',{'id':email[0:-9],'name':first_name+" "+last_name,'email':email,'is_professor':False,'username':'generateUsername()'})
  except:
    print("user already in db")

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

@api_view(['POST'])
@permission_classes([AuthenticatedPermission])
def Logout(request):
  logout(request)
  return redirect('http://localhost:3000')

@api_view(['POST'])
@permission_classes([AuthenticatedPermission])
def RefreshToken(request):
  refresh_token = request.COOKIES.get('refresh_token')
  if not refresh_token:
    return JsonResponse({'error': 'Not valid refresh token'}, status=401)
  
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
  response.set_cookie('access_token', new_access_token, httponly=True)
  response.set_cookie('token_expiration', expires_in)
  response.status_code = 302
  return response