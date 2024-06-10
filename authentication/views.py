from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import http.client
import json
from django.contrib.auth.models import User
from django.contrib.auth import login
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
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
  print(request.session['credentials'])
  conn = http.client.HTTPSConnection("www.googleapis.com")
  headers = {'Authorization': f'Bearer {credentials.token}'}
  conn.request("GET", "/oauth2/v2/userinfo", headers=headers)
  google_response = conn.getresponse()

  user_info = json.loads(google_response.read().decode())
  email = user_info.get('email')
  first_name = user_info.get('given_name')
  last_name = user_info.get('family_name')
  print(email, first_name, last_name)
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
  login(request, user, backend='django.contrib.auth.backends.ModelBackend')
  response = HttpResponse('blah')
  response.set_cookie('token', credentials.token, httponly=True)
  response.set_cookie('refresh_token', credentials.refresh_token, httponly=True)
  response.set_cookie('user_data', json.dumps(user_data))
  response['Location'] = 'http://localhost:3000'
  response.status_code = 302
  return response
