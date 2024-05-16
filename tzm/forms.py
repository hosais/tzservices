# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired
from tzm.model import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.find_by_username(username=username_to_check.data)
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.find_by_email(email_address=email_address_to_check.data)
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')




    username = StringField(label='User Name:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
