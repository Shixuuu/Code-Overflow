from app import app
from flask import render_template, request, redirect, url_for
from app.models import User, db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')