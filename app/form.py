# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo ,ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Sign Up')

    def validate_password(self, field):
        if self.password.data != self.confirm_password.data:
            raise ValidationError('Passwords must match.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
