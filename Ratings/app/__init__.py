import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate

# Initialize the Flask application, the database, and the migration tool
db = SQLAlchemy()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    """
    Creates and configures the Flask application.

    This function initializes the Flask app, sets up the configuration for the 
    application, and initializes the database and migration tools. It also 
    registers the necessary Blueprints for routing.

    Configuration includes:
        - SECRET_KEY: A randomly generated string for securing sessions.
        - SQLALCHEMY_DATABASE_URI: The URI for the MySQL database, using 
          pymysql as the driver.
        - SQLALCHEMY_TRACK_MODIFICATIONS: Disables Flask-SQLAlchemy's 
          modification tracking to save resources.

    This function also imports and registers models and controllers for the 
    application to avoid circular imports.

    Returns:
        Flask: The initialized Flask application instance.
    """
    app = Flask(__name__)

    # Set the secret key for sessions and security (ensure it's a random string)
    app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random 24-byte string for security

    # Use MySQL with the pymysql driver
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MyNewPassword123@localhost/rating'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and migration tool with the app
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    # Import models and controllers here to avoid circular imports
    from app import models, controllers

    # Register controllers (Blueprints)
    app.register_blueprint(controllers.bp)

    return app
