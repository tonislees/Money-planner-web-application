from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from rahaleht.models import User
from rahaleht.main.utils import get_lang, default_lang
from flask_login import current_user


if current_user:
    lang = current_user.language
else:
    lang = default_lang

class registrationForm(FlaskForm):
    username = StringField(get_lang(lang, 'register', 'username'), validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField(get_lang(lang, 'register', 'email'), validators=[DataRequired(), Email()])
    password = PasswordField(get_lang(lang, 'register', 'password'), validators=[DataRequired(), Length(min=8, max=40)])
    confirm_password = PasswordField(get_lang(lang, 'register', 'password2'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(get_lang(lang, 'register', 'signup'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(get_lang(lang, 'errors', 'username_exists'))
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(get_lang(lang, 'errors', 'email_exists'))


class loginForm(FlaskForm):
    user_input = StringField(get_lang(lang, "login", "email"), validators=[DataRequired()])
    password = PasswordField(get_lang(lang, "login", "password"), validators=[DataRequired()])
    remember = BooleanField(get_lang(lang, "login", "remember"))
    submit = SubmitField(get_lang(lang, 'login', 'login'))


class settingsForm(FlaskForm):
    def __init__(self, lang):
        super(settingsForm, self).__init__()
        self.username.label.text = get_lang(lang, "settings", "username")
        self.email.label.text = get_lang(lang, "settings", "email")
        self.language.label.text = get_lang(lang, "settings", "lang")
        self.picture.label.text = get_lang(lang, "settings", "picture_label")
        self.submit.label.text = get_lang(lang, "settings", "save")
    
    language = SelectField("", choices=[('en', 'English'), ('et', 'Eesti')])
    username = StringField("", validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField("", validators=[DataRequired(), Email()])
    picture = FileField("", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    default_picture = BooleanField("")
    submit = SubmitField("")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(get_lang(lang, 'errors', 'username_exists'))
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(get_lang(lang, 'errors', 'email_exists'))


class RequestResetForm(FlaskForm):
    email = StringField(get_lang(lang, "reset_request", "email"), validators=[DataRequired(), Email()])
    submit = SubmitField(get_lang(lang, "reset_request", "request"))

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError(get_lang(lang, "reset_request", "no_account"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(get_lang(lang, "reset_token", "password"), validators=[DataRequired(), Length(min=8, max=40)])
    confirm_password = PasswordField(get_lang(lang, "reset_token", "password2"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(get_lang(lang, "reset_token", "reset"))