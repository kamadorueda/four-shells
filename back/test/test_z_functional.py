def test_functional(
    test_client,
    test_client_with_session,
) -> None:
    # Test home
    response = test_client.get("/")
    assert response.status_code == 200, response.text
    response = test_client_with_session.get("/")
    assert response.status_code == 200, response.text
