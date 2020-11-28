def test_functional(
    test_client,
    test_client_with_session,
) -> None:
    response = test_client.get('/')
    assert response.status_code == 200
    response = test_client_with_session.get('/')
    assert response.status_code == 200

    response = test_client.get('/console/cachipfs')
    assert response.status_code == 500
    response = test_client_with_session.get('/console/cachipfs')
    assert response.status_code == 200
