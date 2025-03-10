from flask import url_for, current_app
from rahaleht import mail
from rahaleht.main.utils import get_lang, default_lang
import secrets, os
from PIL import Image
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, s_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + s_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def delete_picture(picture_file):
    if picture_file != 'default.jpg':
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_file)
        os.remove(picture_path)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(get_lang(default_lang, "reset_token", "email_message"), sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''{get_lang(default_lang, "reset_token", "email_text")}
{url_for('users.reset_token', token=token, _external=True)}
'''
    mail.send(msg)