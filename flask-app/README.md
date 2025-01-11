## Backend (Python/Flask)

### Installation

1. Install the required packages: `pip install flask flask-sqlalchemy flask-jwt-extended flask_cors pyjwt<2.10`
2. Set the `FLASK_APP` environment variable: `export FLASK_APP=app.py`
3. Run the mock data generation script: `python generate_mock_data.py`
4. Start the Flask development server: `flask run`

### Tests

1. `conftest.py`: Sets up pytest fixtures for our tests, including a test client, sample product, sample user, and an authenticated client.
2. `test_models.py`: Tests the creation and basic functionality of our database models (Product, User, and CartItem).
3. `test_routes.py`: Tests the main application routes, including getting products, registering users, logging in, and adding items to the cart.
4. `test_auth.py`: Focuses on testing the authentication system, including user registration, login, and accessing protected routes.

To run these tests, you'll need to install pytest first:

pip install pytest

Then, you can run the tests using the following command in your terminal:

pytest
