import os
import requests
def refresh(refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
    