import os
import requests
from flask import Flask, session, redirect, request, url_for
from oauthlib.oauth2 import WebApplicationClient
from project_code.src.models import User, db

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def get_google_auth_url():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://my-marvel-app.onrender.com/callback",
        scope=["openid", "email", "profile"],
    )
    return request_uri


def get_google_user_info(auth_code):
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=auth_code,
        redirect_uri="https://my-marvel-app.onrender.com/callback",
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

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    return userinfo_response.json()


@app.route("/callback")
def callback():
    code = request.args.get("code")
    user_info = get_google_user_info(code)
    google_id = user_info["sub"]
    email = user_info["email"]

    # Check if the user exists; if not, create a new record
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(google_id=google_id, email=email)
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    return redirect(url_for("game"))


# Other routes like the main game route can go here
@app.route("/game")
def game():
    # Placeholder for game logic
    return "Game Page"
