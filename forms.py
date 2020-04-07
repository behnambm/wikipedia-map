from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import re


class SignupForm(FlaskForm):
    firstname = StringField('First name ', validators=[
                                DataRequired('Please enter your firstname.')
                            ])
    lastname = StringField('Last name', validators=[
                                DataRequired('Please enter your lastname.')
                            ])
    email = StringField('Email', validators=[
                            DataRequired('Please enter your email.'),
                            Email('Your email is invalid.')
                        ])
    password = PasswordField('Password', validators=[
                                DataRequired('Please enter your password'),
                                Length(min=6, message='At least 6 charachters.')
                            ])
    password_confirm = PasswordField('Re-Enter password', validators=[
                                DataRequired('Please re-enter your password.'),
                                Length(min=6, message='At least 6 characters.'),
                                EqualTo('password', message='Passwords must match.')
                            ])
    submit = SubmitField('Sign up')

    @staticmethod
    def validate_password(form, field):
        if not re.findall(r'[a-zA-Z]', field.data):
            msg = '%s should contain at least one character.' %field.name
            raise ValidationError(msg)


class LoginForm(FlaskForm):
    email = StringField('Email ', validators=[DataRequired('Please enter your email.'), Email('Your email is invalid.')])
    password = PasswordField('Password ', validators=[DataRequired('Please enter your password.')])
    submit = SubmitField('Login')


class AddressForm(FlaskForm):
    address = StringField('Address', 
        validators=[
            DataRequired('Please enter address.')], 
        render_kw={'placeholder':'ex. New York'})

    radius = IntegerField('Radius', 
        validators=[
            DataRequired('Please enter radius.') ],
            render_kw={'placeholder': 'Default 5000'})

    @staticmethod
    def validate_radius(form, field):
        data = field.data
        if not (data >= 10 and data <= 10000):
            msg = '%s must be 10-10000.' %field.name
            raise ValidationError(msg)

    submit = SubmitField('Search')