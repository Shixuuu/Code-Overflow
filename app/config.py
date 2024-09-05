import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
WTF_CSRF_ENABLED = True

class Config:
    # Base configuration class
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF protection
    


app = Flask(__name__)

# Configuration of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite as an example
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)