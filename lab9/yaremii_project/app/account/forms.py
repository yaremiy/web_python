from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(
                                           min=4, max=14, message='Name length must be between %(min)d and %(max)d'),
                                       Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                                              message='Username can contains lettes, numbers, dots and underscores')])
    email = StringField("Email", validators=[
                        DataRequired(), Email(message='Email is invalid')])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6,
                                                                message='Password must be longer than 6 symbols')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        DataRequired(), Email(message='Email is invalid')])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")
