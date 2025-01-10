import sys
import os
import json
import pytest
from app import app, db
from models import Product

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ecommerce.db'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def sample_product():
    return Product(title="Test Product", description="Test Description", price=10.0, category="Test Category", image_url="http://example.com/image.jpg", stock=10)

def test_get_products(client, sample_product):
    with app.app_context():
        db.session.add(sample_product)
        db.session.commit()

    response = client.get('/api/products')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['products']) == 1
    assert data['products'][0]['title'] == "Test Product"

def test_get_product(client, sample_product):
    with app.app_context():
        db.session.add(sample_product)
        db.session.commit()
        product_id = sample_product.id

    response = client.get(f'/api/products/{product_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == "Test Product"

# def test_get_cart(authenticated_client, sample_product):
#     with app.app_context():
#         db.session.add(sample_product)
#         db.session.commit()

#         # Add item to cart
#         authenticated_client.post('/api/cart/add', json={
#             'product_id': sample_product.id,
#             'quantity': 1
#         })

#     response = authenticated_client.get('/api/cart')
#     assert response.status_code == 200
#     data = json.loads(response.data)
#     assert len(data) == 1
#     print(data[0]['product_id'])
#     assert data[0]['product_id'] == sample_product.id
#     assert data[0]['quantity'] == 1