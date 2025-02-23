from flask import Blueprint, render_template, url_for, flash, redirect, request
from rahaleht.models import User
from rahaleht.users.forms import loginForm, registrationForm, settingsForm, RequestResetForm, ResetPasswordForm
from rahaleht import db, bcrypt
from rahaleht.users.utils import save_picture, delete_picture, send_reset_email
from rahaleht.main.utils import get_lang, default_lang	
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)

@users.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{get_lang(default_lang, 'register', 'username_exists')} {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, current_path=request.path, get_lang=get_lang, lang=default_lang)


@users.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = loginForm()
    if form.validate_on_submit():
        user_by_username = User.query.filter_by(username=form.user_input.data).first()
        user_by_email = User.query.filter_by(email=form.user_input.data).first()
        if user_by_username and bcrypt.check_password_hash(user_by_username.password, form.password.data):
            login_user(user_by_username, remember=form.remember.data)
            return redirect(url_for('main.home'))
        elif user_by_email and bcrypt.check_password_hash(user_by_email.password, form.password.data):
            login_user(user_by_email, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash(get_lang(default_lang, 'login', 'unsuccesful'), 'danger')
    return render_template('login.html', title='Log in', form=form, current_path=request.path, get_lang=get_lang, lang=default_lang)


@users.route("/logout", methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/settings", methods=['POST', 'GET'])
@login_required
def settings():
    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    form = settingsForm(current_user.language)
    flash_message = False
    if form.validate_on_submit():
        if (form.default_picture.data and current_user.image_file != 'default.jpg') or form.picture.data or (current_user.email != form.email.data) or (current_user.username != form.username.data) or (current_user.language != form.language.data):
            flash_message = True
        if form.picture.data:
            delete_picture(current_user.image_file)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        elif form.default_picture.data:
            delete_picture(current_user.image_file)
            current_user.image_file = 'default.jpg'
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.language = form.language.data
        db.session.commit()
        if flash_message:
            flash(get_lang(current_user.language, "settings", "changes_saved"), 'success')
        return redirect(url_for('users.settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.language.data = current_user.language
    return render_template('settings.html', current_path=request.path, 
                           img_file=img_file, form=form, lang=current_user.language, 
                           get_lang=get_lang)


@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form, lang=default_lang, get_lang=get_lang)


@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'Token not valid', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash(get_lang(default_lang, "reset_token", "reset_done"), 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form, lang=default_lang, get_lang=get_lang)