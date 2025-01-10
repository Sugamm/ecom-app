import pytest
from models import Product, User, CartItem
from werkzeug.security import check_password_hash

def test_product_creation(sample_product):
    assert sample_product.title == "Test Product"
    assert sample_product.price == 10.99
    assert sample_product.stock == 5

def test_user_creation(sample_user):
    assert sample_user.name == "Test User"
    assert sample_user.email == "test@example.com"
    assert check_password_hash(sample_user.password_hash, "testpassword")

def test_cart_item_creation(sample_user, sample_product):
    cart_item = CartItem(user_id=sample_user.id, product_id=sample_product.id, quantity=2)
    assert cart_item.user_id == sample_user.id
    assert cart_item.product_id == sample_product.id
    assert cart_item.quantity == 2

