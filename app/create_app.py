from flask import Flask
from flask_hashing import Hashing
from flask_cors import CORS
from flask_redis import FlaskRedis
import os
if os.getenv("SENTRY_DSN"):
    from sentry_sdk.integrations.flask import FlaskIntegration
    import sentry_sdk


def create_app():
    if os.getenv("SENTRY_DSN"):
        sentry_sdk.init(
            dsn=os.environ["SENTRY_DSN"],
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )
    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET"]
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        REDIS_URL=os.environ["REDIS_URL"],
        VERSION="0.0.1",
        UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", "/tmp")
    )
    CORS(app,
         methods=["GET", "POST", "OPTIONS"],
         supports_credential=True)
    app.redis_client = FlaskRedis(app)
    app.hashing = Hashing(app)
    return app
