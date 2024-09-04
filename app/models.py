from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_login = db.Column(db.Boolean, default=True)  # New field to track first login
    sector = db.Column(db.String(50))
    money = db.Column(db.Integer, default=5000)
    friends = db.relationship('Friend', backref='user', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)
    friend_name = db.Column(db.String(80), nullable=False)
    friend_image = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<Friend {self.friend_name}>'