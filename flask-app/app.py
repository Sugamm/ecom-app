from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models import db, Product, User, CartItem
from sqlalchemy import func
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'ecom-secret-key')  # Change this in production
jwt = JWTManager(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, world!'})


@app.route('/api/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    search = request.args.get('search')

    query = Product.query

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.title.ilike(f'%{search}%'))

    products = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'products': [
            {
                'id': p.id,
                'title': p.title,
                'price': p.price,
                'category': p.category,
                'image_url': p.image_url,
                'stock': p.stock
            } for p in products.items
        ],
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    })

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'price': product.price,
        'category': product.category,
        'image_url': product.image_url,
        'stock': product.stock
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': item.id,
            'product_id': item.product_id,
            'title': item.product.title,
            'price': item.product.price,
            'quantity': item.quantity,
            'stock': item.product.stock
        } for item in cart_items
    ])

@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.json
    product = Product.query.get_or_404(data['product_id'])
    
    if product.stock < data['quantity']:
        return jsonify({'message': 'Not enough stock'}), 400

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=data['product_id']).first()
    if cart_item:
        cart_item.quantity += data['quantity']
    else:
        cart_item = CartItem(user_id=user_id, product_id=data['product_id'], quantity=data['quantity'])
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart'}), 200

@app.route('/api/cart/update', methods=['PUT'])
@jwt_required()
def update_cart():
    user_id = get_jwt_identity()
    data = request.json
    cart_item = CartItem.query.filter_by(id=data['cart_item_id'], user_id=user_id).first_or_404()
    
    if cart_item.product.stock < data['quantity']:
        return jsonify({'message': 'Not enough stock'}), 400

    cart_item.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Cart updated successfully'}), 200

@app.route('/api/cart/remove', methods=['DELETE'])
@jwt_required()
def remove_from_cart():
    user_id = get_jwt_identity()
    data = request.json
    cart_item = CartItem.query.filter_by(id=data['cart_item_id'], user_id=user_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200

if __name__ == '__main__':
    app.run(debug=True)