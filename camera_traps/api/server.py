import datetime
from urllib.parse import urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, request, session, url_for

from camera_traps.settings import S

server = Flask(__name__)


server.config.update(
    SECRET_KEY=S.FLASK_SECRET_KEY,
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=7),
)

oauth = OAuth(server)
auth0 = oauth.register(
    name="auth0",
    client_id=S.AUTH_CLIENT_ID,
    client_secret=S.AUTH_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{S.AUTH_DOMAIN}/.well-known/openid-configuration",
)


@server.route("/login")
def login():
    """Send the user to the Auth0 login page"""

    redirect_uri = url_for("authorize", _external=True)
    return auth0.authorize_redirect(redirect_uri=redirect_uri)


@server.route("/authorize")
def authorize():
    """Handle the Auth0 redirect after login and save user info in the session"""

    token = auth0.authorize_access_token()
    session.permanent = True
    session["user"] = token["userinfo"]
    return redirect("/")


@server.route("/logout")
def logout():
    """Clear the local session and log the user out of Auth0 as well"""

    session.clear()
    params = {
        "returnTo": url_for("login", _external=True),
        "client_id": S.AUTH0_CLIENT_ID,
    }
    return redirect(f"https://{S.AUTH_DOMAIN}/v2/logout?{urlencode(params)}")


@server.before_request
def require_login():
    """Enforce login on all endpoints except auth routes, static files, etc"""

    if request.endpoint in ("login", "authorize", "logout", "static"):
        return None

    if "user" not in session:
        return redirect(url_for("login"))

    return None
