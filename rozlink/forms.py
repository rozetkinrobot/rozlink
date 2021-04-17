from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
# from wtforms.widgets import PasswordInput


class BaseForm(FlaskForm):
    @property
    def error_list(self):
        _errors = []
        for fieldName, errorMessages in self.errors.items():
            for err in errorMessages:
                _errors.append(err)
        return _errors


class LoginForm(BaseForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(BaseForm):
    login = StringField('Login', validators=[
                        DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', validators=[
                        DataRequired(), Email(), Length(min=6, max=64)])
    password = PasswordField('Password', validators=[DataRequired(),  Length(min=4), EqualTo('password2',
                                                                                             message='Passwords must match')])
    password2 = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class ChangePassForm(BaseForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(),  Length(min=4), EqualTo('password2',
                                                                                                 message='New passwords must match')])
    password2 = PasswordField('Repeat new password',
                              validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LinkForm(BaseForm):
    link = StringField('link', validators=[DataRequired()])
    submit = SubmitField('Submit')
