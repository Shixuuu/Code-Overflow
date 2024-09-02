from flask import Flask, render_template
from sqlalchemy import create_engine

engine = create_engine('sqlite:///example.db',echo = True)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', active_page='home')
@app.route('/about')
def about():
    return render_template('about.html',active_page='about')

if __name__ == "__main__":
    app.run(debug=True)