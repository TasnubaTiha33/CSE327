import os

class Config:
    """
    Base configuration class for the application.

    This class contains configuration settings for the application. 
    It reads the configuration values from environment variables, providing 
    flexibility for different environments (development, production, etc.).

    Attributes:
        SECRET_KEY (str): Secret key used for session management. It should be set to a secure, 
                          random value in production for cryptographic operations. Defaults to 
                          'your_secret_key' if not set in the environment.
        DB_HOST (str): Hostname of the database server. Defaults to 'localhost' if not set in the environment.
        DB_USER (str): Database username. Defaults to 'root', commonly used for local MySQL installations.
        DB_PASSWORD (str): Database password. Leave empty if no password is set.
        DB_NAME (str): Name of the database. Defaults to 'review' if not set in the environment.

    Example:
        To use a custom configuration in production, you can set the environment variables:
        ```bash
        export SECRET_KEY='your_real_secret_key'
        export DB_HOST='db.example.com'
        export DB_USER='your_db_user'
        export DB_PASSWORD='your_db_password'
        export DB_NAME='your_database_name'
        ```

    Note:
        It's highly recommended to set the environment variables in a secure manner, 
        especially for production environments, and avoid hardcoding sensitive information.
    """
    # Secret key for session management (Change this to a real secret key in production)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')  # Use environment variable in production
    
    # Database connection settings
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')  # Default username for MySQL is often 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')  # Leave empty if no password
    DB_NAME = os.environ.get('DB_NAME', 'review')  # Database name (update if necessary)
    
    # Optionally add other configuration settings (e.g., for mail, logging, etc.)
    # MAIL_SERVER = 'smtp.mailtrap.io'  # Example of mail server configuration (optional)
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
