def test_functional(
    test_client,
    test_client_with_session,
    test_client_with_session_raiser,
) -> None:
    response = test_client.get('/')
    assert response.status_code == 200, response.text
    response = test_client_with_session.get('/')
    assert response.status_code == 200, response.text

    response = test_client.get('/console/cachipfs')
    assert response.status_code == 500, response.text
    response = test_client_with_session.get('/console/cachipfs')
    assert response.status_code == 200, response.text

    # List namespaces
    response = test_client_with_session_raiser.get('/api/v1/cachipfs/namespaces')
    assert response.status_code == 200, response.text

    # Delete all namespaces
    for namespace_id in response.json():
        response = test_client_with_session_raiser.delete(f'/api/v1/cachipfs/namespace/{namespace_id}')
        assert response.status_code == 200, response.text

    # Create namespace
    response = test_client_with_session.post('/api/v1/cachipfs/namespace/test')
    assert response.status_code == 200, response.text
    namespace = response.json()

    # List namespaces
    response = test_client_with_session_raiser.get('/api/v1/cachipfs/namespaces')
    assert response.status_code == 200, response.text
    assert response.json() == [namespace['id']]
