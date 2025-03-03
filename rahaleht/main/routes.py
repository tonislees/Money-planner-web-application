from flask import render_template, Blueprint
from rahaleht.main.utils import get_lang, default_lang
from flask_login import current_user


main = Blueprint('main', __name__)

@main.route("/home")
def home():
    if current_user.is_authenticated:
        lang = current_user.language
    else:
        lang = default_lang
    return render_template('home.html', get_lang=get_lang, lang=lang)