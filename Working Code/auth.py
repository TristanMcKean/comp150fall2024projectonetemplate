from requests_oauthlib import OAuth2Session
from flask import url_for, redirect
import os


# Load environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Google OAuth 2.0 URLs
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

def get_google_auth_url():
    """
    Generate the Google authorization URL for OAuth.
    """
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["openid", "email", "profile"])
    auth_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline", prompt="consent")
    return auth_url

def get_google_user_info(auth_code):
    """
    Exchange the authorization code for a token and retrieve the user's info.
    :param auth_code: The authorization code returned by Google after login.
    :return: A dictionary containing the user's Google profile information.
    """
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = google.fetch_token(TOKEN_URL, client_secret=GOOGLE_CLIENT_SECRET, code=auth_code)

    # Fetch user information
    google = OAuth2Session(GOOGLE_CLIENT_ID, token=token)
    user_info = google.get(USER_INFO_URL).json()
    return {
        "email": user_info.get("email"),
        "name": user_info.get("name")
    }
