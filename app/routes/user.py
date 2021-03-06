from app import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
import app.forms as forms
from app.models import Users
from app import generate_token
from flask_login import logout_user, login_user, current_user


@app.route('/documentation', methods=['GET', 'POST'])
def docs():
    """Возвращает страницу с документацией к Api"""
    token_form = forms.AuthForm()
    if current_user.is_authenticated:
        # Сразу отображает токен пользователя в поле, если пользователь уже вошёл в систему.
        email = current_user.email
        return render_template('documentation.html', title='Documentation', form=token_form,
                               message=Users.query.filter_by(email=email).first().token)

    if token_form.validate_on_submit():
        user = Users.query.filter_by(email=token_form.email.data).first()
        if not user:
            flash('Вы не зарегистрированы.')
            return redirect(url_for('docs'))

        if not check_password_hash(Users.query.filter_by(email=token_form.email.data).first().password_hash,
                                   token_form.password.data):
            flash('Пароль не верный.')
            return redirect(url_for('docs'))

        message = user.token
        return render_template('documentation.html', title='Documentation', form=token_form, message=message)
    return render_template('documentation.html', title='Documentation', form=token_form)


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    """Возвращает страницу с регистрацией"""
    if current_user.is_authenticated:
        return render_template('after_login.html')
    registration_data = forms.RegistrationForm()
    if registration_data.validate_on_submit():
        if Users.query.filter_by(email=registration_data.email.data).first():
            flash('Пользователь c таким email-адресом уже существует.')
            return redirect(url_for('reg'))

        user = Users(id=Users.query.count() + 1, email=registration_data.email.data,
                     password_hash=generate_password_hash(registration_data.password.data),
                     token=generate_token.generate_token())
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались.')
        login_user(user, remember=registration_data.remember_me.data)
        return render_template('after_login.html')
    return render_template('registration.html', title='registration', form=registration_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница аутентификации"""
    if current_user.is_authenticated:
        return render_template('after_login.html')
    login_data = forms.LoginForm()
    if login_data.validate_on_submit():
        user = Users.query.filter_by(email=login_data.email.data).first()
        if not user:
            flash('Вы не зарегистрированы.')
            return redirect(url_for('login'))

        if not check_password_hash(Users.query.filter_by(email=login_data.email.data).first().password_hash,
                                   login_data.password.data):
            flash('Пароль не верный.')
            return redirect(url_for('login'))

        login_user(user, remember=login_data.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return render_template('after_login.html')
        return redirect(next_page)
    return render_template('login.html', title='login', form=login_data)


@app.route('/logout')
def logout():
    """Страница выхода пользователя"""
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('login'))
