from authlib.integrations.flask_client import OAuth
from config import config

oauth = OAuth()

def configure_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        access_token_url=config.ACCESS_TOKEN_URL,
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        client_kwargs={
            "scope": "openid email profile",
        },
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"  # ✅ Fix: Adds necessary metadata
    )

    return oauth
