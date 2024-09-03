import sys
import os

# Ensure the project root directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

with app.app_context():
    db.create_all()