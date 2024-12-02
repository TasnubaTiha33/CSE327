from flask import Flask
from flask_login import LoginManager
from .models import User  # Only import models after db is initialized
from flask_sqlalchemy import SQLAlchemy
import os
print("Template folder path:", os.path.join(os.getcwd(), "views"))

db = SQLAlchemy()

# Initialize database and login manager
login_manager = LoginManager()

def create_app(config_class="config.DevelopmentConfig"):

    app = Flask(__name__, template_folder='views')
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "error"

    from .controllers import routes
    app.register_blueprint(routes)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
