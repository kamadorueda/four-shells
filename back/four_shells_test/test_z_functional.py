def test_functional(
    test_client,
    test_client_with_session,
    test_client_session,
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
    response = test_client_session.get('/api/v1/cachipfs/namespaces')
    assert response.status_code == 200, response.text

    # Delete all namespaces
    for namespace in response.json():
        namespace_id = namespace['id']
        response = test_client_session.delete(f'/api/v1/cachipfs/namespace/{namespace_id}')
        assert response.status_code == 200, response.text

    # List namespaces
    response = test_client_session.get('/api/v1/cachipfs/namespaces')
    assert response.status_code == 200, response.text
    assert response.json() == []

    # Create namespace
    response = test_client_with_session.post('/api/v1/cachipfs/namespace/test')
    assert response.status_code == 200, response.text
    namespace = response.json()
    namespace_id = namespace['id']

    # List namespaces
    response = test_client_session.get('/api/v1/cachipfs/namespaces')
    assert response.status_code == 200, response.text
    assert response.json()[0]['id'] == namespace_id, response.json()

    # Get namespace
    response = test_client_session.get(f'/api/v1/cachipfs/namespace/{namespace_id}')
    assert response.status_code == 200, response.text
    assert response.json()['id'] == namespace_id, response.json()
    assert 'name' in response.json(), response.json()
    assert 'token_admin' in response.json(), response.json()
    assert 'token_read' in response.json(), response.json()
    assert 'token_write' in response.json(), response.json()

    # Rotate tokens
    token_admin = response.json()['token_admin']
    token_read = response.json()['token_read']
    token_write = response.json()['token_write']
    for entity in {
        'token_admin',
        'token_read',
        'token_write',
    }:
        response = test_client_session.post(f'/api/v1/cachipfs/namespace/{namespace_id}/rotate/{entity}')
        assert response.status_code == 200, response.text
    response = test_client_session.get(f'/api/v1/cachipfs/namespace/{namespace_id}')
    assert response.status_code == 200, response.text
    assert response.json()['token_admin'] != token_admin
    assert response.json()['token_read'] != token_read
    assert response.json()['token_write'] != token_write
