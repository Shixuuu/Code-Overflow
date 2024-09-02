from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config  # Import the config from config.py

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)  # Apply configuration

# Initialize the database
db = SQLAlchemy(app)

# Import routes and models
from app import routes, models
