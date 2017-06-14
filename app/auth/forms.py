# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import User


class LoginForm(Form):
    email = StringField(u"邮箱", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u"密码", validators=[DataRequired()])
    rember_me = BooleanField(u"记住")
    submit = SubmitField(u'登录')

# class RegistrationForm(Form):
#     email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
#     username = StringField("Username", validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
#                                                                                          "Username must be have only letters")])
#     password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2', "Password must be match")])
#     password2 = PasswordField("Confirm Password", validators=[DataRequired()])
#     submit = SubmitField('Register')
#
#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data).first():
#             raise ValidationError('Email already registered.')
#     def validate_username(self, field):
#         if User.query.filter_by(username=field.data).first():
#             raise ValidationError("Username already registered")
