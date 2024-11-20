from flask import Flask

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure app using settings from config.py
    app.config.from_object('config.Config')

    # Import and register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
