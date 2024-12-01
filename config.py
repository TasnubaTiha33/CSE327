import os

class Config:
    # Secret key to manage sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'

    # SQLAlchemy configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost/book_vault'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    # Development specific configurations
    DEBUG = True

class ProductionConfig(Config):
    # Production specific configurations
    DEBUG = False
