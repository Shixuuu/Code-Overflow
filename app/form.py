# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email,ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Sign Up')

    def validate_password(self, field):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords must match.')
        if len(self.password.data) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
        if not '@' in field.data:
            raise ValidationError('Invalid email address.')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
        if len(field.data) < 5: 
            raise ValidationError('Username must be at least 5 characters long.')   

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
