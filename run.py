import sys
import os

# Add the project directory to sys.path
project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_dir)

from app import create_app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)

