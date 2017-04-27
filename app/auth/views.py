from flask import render_template, redirect, url_for, request, flash
from . import auth
from forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.semail import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.vertify_password(form.password.data):
            login_user(user, form.rember_me.data)
            return redirect(request.args.get('next') or url_for('mian.index'))
        flash("Invalid username or password")
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("You hava been loggde out")
    return render_template(url_for('mian.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email, "Confirm Your Account", 'auth/email/confirm', user=user, token=token)
        flash("A confirm email has been sent to you by email.")

        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed():
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash("You have confirm you account, thanks!")
    else:
        flash("The confirmation link is invalid or has expired")
    return redirect(url_for('main.index'))
