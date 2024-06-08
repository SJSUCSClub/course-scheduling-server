from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
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
    response = HttpResponse('blah')
    response.set_cookie('token', credentials.token, httponly=True)
    response.set_cookie('refresh_token', credentials.refresh_token, httponly=True)
    return response

