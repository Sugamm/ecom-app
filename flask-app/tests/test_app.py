import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from app import app
from models import db, Product, User, CartItem

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_products(self):
        with app.app_context():
            product = Product(title="Test Product", price=10.99, category="Test Category", stock=5)
            db.session.add(product)
            db.session.commit()

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['products']), 1)
        self.assertEqual(data['products'][0]['title'], "Test Product")

    def test_get_product(self):
        with app.app_context():
            product = Product(title="Test Product", price=10.99, category="Test Category", stock=5)
            db.session.add(product)
            db.session.commit()
            product_id = product.id

        response = self.client.get(f'/api/products/{product_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Product")

    def test_register(self):
        response = self.client.post('/api/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User registered successfully')

    def test_login(self):
        with app.app_context():
            user = User(name="Test User", email="test@example.com")
            user.set_password("testpassword")
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/api/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

if __name__ == '__main__':
    unittest.main()

