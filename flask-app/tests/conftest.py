import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from models import db, Product, User, CartItem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_product():
    product = Product(title="Test Product", description="Test Description", price=10.99, category="Test Category", image_url="http://test.com/image.jpg", stock=5)
    return product

@pytest.fixture
def sample_user():
    user = User(name="Test User", email="test@example.com")
    user.set_password("testpassword")
    return user

@pytest.fixture
def authenticated_client(client, sample_user):
    with app.app_context():
        db.session.add(sample_user)
        db.session.commit()

    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    access_token = response.json['access_token']
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client

