import os
import sys
from pathlib import Path

import pytest
from betamax import Betamax
from flask.testing import FlaskClient
from flask_dance.consumer.storage import MemoryStorage
from flask_dance.contrib.google import google

toplevel = Path(__file__).parent.parent
sys.path.insert(0, str(toplevel))
from app import app as flask_app
from app.oauth import blueprint
from app.models import db, User, OAuth


GOOGLE_ACCESS_TOKEN = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN", "fake-token")

with Betamax.configure() as config:
    config.cassette_library_dir = toplevel / "tests" / "cassettes"
    config.define_cassette_placeholder("<AUTH_TOKEN>", GOOGLE_ACCESS_TOKEN)


class FlaskLoginClient(FlaskClient):
    """
    A Flask test client that knows how to log in users
    using the Flask-Login extension.
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        fresh = kwargs.pop("fresh_login", True)

        super(FlaskLoginClient, self).__init__(*args, **kwargs)

        if user:
            with self.session_transaction() as sess:
                sess["user_id"] = user.id
                sess["_fresh"] = fresh


@pytest.fixture
def google_authorized(monkeypatch):
    """
    Monkeypatch the GitHub Flask-Dance blueprint so that the
    OAuth token is always set.
    """
    storage = MemoryStorage({"access_token": GOOGLE_ACCESS_TOKEN})
    monkeypatch.setattr(blueprint, "storage", storage)
    return storage


@pytest.fixture(scope="session")
def app():
    flask_app.test_client_class = FlaskLoginClient
    return flask_app


@pytest.fixture(scope="session")
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture
def flask_dance_sessions():
    """
    Necessary to use the ``betamax_record_flask_dance`` fixture
    from Flask-Dance
    """
    return google


@pytest.fixture
def user(db_session):
    u = User(email="test@example.com")
    oauth = OAuth(
        user=u,
        provider="google",
        provider_user_id="12345",
        token={"access_token": GOOGLE_ACCESS_TOKEN},
    )
    db_session.add_all([u, oauth])
    db_session.commit()
    return u
