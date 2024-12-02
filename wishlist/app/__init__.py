from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database and login manager globally
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Setup database URI and other configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize the extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Register the wishlist blueprint
    from app.wishlist import wishlist_bp  # Ensure this is correctly imported
    app.register_blueprint(wishlist_bp)

    # Setup the login_view for Flask-Login
    login_manager.login_view = 'auth.login'  # Ensure the login route exists in your app

    # Import views (templates) setup
    app.jinja_env.globals.update(zip=zip)

    return app
