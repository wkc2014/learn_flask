from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import Length, DataRequired, Email, Regexp
from app.models import User, Role
from flask_pagedown.fields import PageDownField

class EditPofileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('about_me')
    submit = SubmitField('Submit')


class EditPofileFormAdmin(Form):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         "Username must be have only letters")])
    name = StringField('Real name', validators=[Length(0, 64)])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('about_me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditPofileFormAdmin, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() and field.data != self.user.email:
            raise ValueError("Email already registered")

    def validate_username(self, field):
        if User.query.filter_by(email=field.data).first() and field.data != self.user.username:
            raise ValueError("Username already registered")


class PostForm(Form):
    body = PageDownField("what's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReadForm(Form):
    submit = SubmitField('Read')
