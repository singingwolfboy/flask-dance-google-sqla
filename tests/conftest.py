import os
import sys
from pathlib import Path

import pytest
from betamax import Betamax
from flask.testing import FlaskClient

toplevel = Path(__file__).parent.parent
sys.path.insert(0, str(toplevel))
from app import app as flask_app
from app.oauth import blueprint as _blueprint
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
def google_access_token():
    return GOOGLE_ACCESS_TOKEN


@pytest.fixture
def blueprint(request):
    token = {"access_token": GOOGLE_ACCESS_TOKEN}
    # avoid "Cannot get OAuth token without an associated user" error
    _blueprint.session.token = token
    # wrap session with Betamax
    recorder = Betamax(_blueprint.session)
    with recorder.use_cassette(request.node.name):
        yield _blueprint


@pytest.fixture(scope="session")
def app():
    flask_app.test_client_class = FlaskLoginClient
    return flask_app


@pytest.fixture(scope="session")
def _db(app):
    """
    Necessary to use the ``db_session`` fixture
    from pytest-flask-sqlalchemy
    """
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()


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
