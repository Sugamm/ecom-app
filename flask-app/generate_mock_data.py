from app import app, db
from models import Product, User
import random

categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Toys']
adjectives = ['Amazing', 'Incredible', 'Fantastic', 'Wonderful', 'Awesome']
nouns = ['Widget', 'Gadget', 'Tool', 'Device', 'Accessory']

def generate_mock_data():
    with app.app_context():
        # Generate products
        for _ in range(500):
            product = Product(
                title=f"{random.choice(adjectives)} {random.choice(nouns)}",
                description="This is a product description.",
                price=round(random.uniform(10, 1000), 2),
                category=random.choice(categories),
                image_url=f"https://picsum.photos/200/300?random={random.randint(1, 1000)}",
                stock=random.randint(0, 100)
            )
            db.session.add(product)

        # Generate users
        for i in range(5):
            user = User(name=f"User {i+1}", email=f"user{i+1}@example.com")
            user.set_password("password123")
            db.session.add(user)

        db.session.commit()

if __name__ == '__main__':
    generate_mock_data()