def test_index_unauthorized(app):
    with app.test_client() as client:
        response = client.get("/", base_url="https://example.com")

    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "You are not logged in" in text


def test_index_authorized(app, user):
    with app.test_client(user=user) as client:
        response = client.get("/", base_url="https://example.com")

    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "You are logged in as test@example.com!" in text
