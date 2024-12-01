# app.py

"""
This module contains the entry point for the BookVault application.

It imports the `create_app` function from the `app` package, creates a Flask
application instance, and runs the application in debug mode.

The `create_app` function is responsible for configuring the Flask app, setting
up the necessary extensions (such as SQLAlchemy and Flask-Migrate), and registering
blueprints and other components of the application.

The app is set to run in debug mode when executed directly.
"""

from app import create_app

# Create the Flask app using the app factory
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)
