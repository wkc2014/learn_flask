from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from app.models import User

class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    rember_me = BooleanField("Keep me logged in")
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField("Username", validators=[DataRequired(),Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,"Username must be have only letters")])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2',"Password must be match")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError("Email already registered")
    def validate_username(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError("Username already registered")