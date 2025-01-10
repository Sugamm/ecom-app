
import json

def test_register_and_login(client):
    # Test registration
    register_response = client.post('/api/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert register_response.status_code == 201
    register_data = json.loads(register_response.data)
    assert register_data['message'] == 'User registered successfully'

    # Test login
    login_response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert login_response.status_code == 200
    login_data = json.loads(login_response.data)
    assert 'access_token' in login_data

def test_invalid_login(client):
    response = client.post('/api/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'Invalid credentials'

# def test_protected_route(client, authenticated_client):
#     # Test accessing a protected route without token
#     response = client.get('/api/cart')
#     print("jello")
#     print(response.status_code)
#     assert response.status_code == 401

#     # Test accessing a protected route with token
#     response = authenticated_client.get('/api/cart')
#     assert response.status_code == 200

