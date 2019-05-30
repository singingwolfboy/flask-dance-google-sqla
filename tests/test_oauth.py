import pytest
import flask
from app.models import User, OAuth
from app.oauth import google_logged_in

# All tests in this file should be wrapped in database transactions
pytestmark = pytest.mark.usefixtures("db_session")


def test_oauth_create_user(app, blueprint, google_access_token):
    token = {"access_token": google_access_token}
    assert User.query.count() == 0
    assert OAuth.query.count() == 0

    with app.test_request_context("/login/google/authorized"):
        returned = google_logged_in(blueprint, token)
        logged_in_uid = flask.session.get("user_id")

    assert returned is False
    assert User.query.count() == 1
    assert OAuth.query.count() == 1
    oauth = OAuth.query.first()
    assert oauth.provider == "google"
    assert oauth.provider_user_id == "106473082171117460211"
    assert oauth.token == token
    user = oauth.user
    assert user.email == "david@davidbaumgold.com"
    assert logged_in_uid == str(user.id)


def test_oauth_login_user(db_session, app, blueprint, google_access_token):
    token = {"access_token": google_access_token}

    user = User(email="david@davidbaumgold.com")
    oauth = OAuth(
        user=user,
        provider="google",
        provider_user_id="106473082171117460211",
        token=token,
    )
    db_session.add_all([user, oauth])
    db_session.commit()
    assert User.query.count() == 1
    assert OAuth.query.count() == 1

    with app.test_request_context("/login/google/authorized"):
        returned = google_logged_in(blueprint, token)
        logged_in_uid = flask.session.get("user_id")

    assert returned is False
    # counts are unchanged
    assert User.query.count() == 1
    assert OAuth.query.count() == 1
    assert logged_in_uid == str(user.id)
