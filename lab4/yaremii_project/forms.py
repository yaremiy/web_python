from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, Regexp


class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired("Please enter your name"),
                                           Length(min=4, max=10)])
    email = StringField("Email", validators=[DataRequired(
        "Please enter your email"), Email(message='Email is invalid')])
    phone = StringField("Phone", validators=[DataRequired("Please enter your phone number"),
                        Regexp(regex='^\+380[0-9]{9}$', message='Phone is invalid')])
    subject = SelectField("Subject", choices=[
                          ('1', 'Job offer'), ('2', 'Business'), ('3', 'Compliment')])
    message = TextAreaField("Message", validators=[DataRequired(
        "Please enter the message"), Length(max=500, message='Message is too long')])
    submit = SubmitField("Send")
