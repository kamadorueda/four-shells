def test_functional(
    test_client,
    test_client_with_session,
) -> None:
    # Test home
    response = test_client.get('/')
    assert response.status_code == 200, response.text
    response = test_client_with_session.get('/')
    assert response.status_code == 200, response.text

    # Test cachipfs home
    response = test_client.get('/cachipfs')
    assert response.status_code == 200, response.text
    response = test_client_with_session.get('/cachipfs')
    assert response.status_code == 200, response.text

    # Test cachipfs dashboard
    response = test_client.get('/cachipfs/dashboard')
    assert response.status_code == 200, response.text
    response = test_client_with_session.get('/cachipfs/dashboard')
    assert response.status_code == 200, response.text

    # Test /api/v1/me
    response = test_client_with_session.get('/api/v1/me')
    assert response.status_code == 200, response.text
    response = response.json()
    cachipfs_api_token = response['cachipfs_api_token']
    assert cachipfs_api_token
    cachipfs_trusted_ids = response['cachipfs_trusted_ids']
    assert cachipfs_trusted_ids
    cachipfs_id = response['cachipfs_id']
    assert cachipfs_id
    email = response['email']
    assert email
