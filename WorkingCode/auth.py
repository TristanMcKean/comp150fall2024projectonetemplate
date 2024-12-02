import os
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://marvel-heroes-adventure.onrender.com/callback")  # Dynamically use testing or production URI
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Ensure the environment variables are set
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Google Client ID and Secret must be set in environment variables.")

# Initialize the OAuth2 client
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    """Fetch Google's OAuth provider configuration."""
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch Google provider configuration: {e}")

def get_google_auth_url():
    """Generate the Google Sign-In URL."""
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    try:
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=REDIRECT_URI,  # Use environment variable for dynamic configuration
            scope=["openid", "email", "profile"],
        )
        return request_uri
    except Exception as e:
        raise RuntimeError(f"Failed to generate Google Sign-In URL: {e}")

def get_google_user_info(auth_code):
    """Fetch the user's Google account information using the authorization code."""
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    try:
        # Prepare and send token request
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=f"{REDIRECT_URI}?code={auth_code}",
            redirect_url=REDIRECT_URI,  # Explicitly pass the redirect_uri
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        client.parse_request_body_response(token_response.text)

        # Use the access token to fetch user info
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.status_code != 200:
            raise RuntimeError(f"Failed to fetch user info: {userinfo_response.text}")

        return userinfo_response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch user info: {e}")

