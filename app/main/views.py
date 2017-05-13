from app.decorators import admin_required
from . import main
from .forms import EditPofileForm, EditPofileFormAdmin
from flask import render_template, abort, redirect, url_for, flash
from app.models import User, db, Role
from flask_login import current_user, login_required


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/article', methods=['GET', 'POST'])
def article():
    return render_template('article.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditPofileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('You profile has been update')
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me

    return render_template('edit-profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditPofileFormAdmin(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.username = form.username.data
        user.email = form.email.data
        user.role = Role.query.get(form.role.data)
        user.confirmed = form.confirmed.data
        db.session.add(user)
        flash('You profile has been update')
        db.session.commit()
        return redirect(url_for('main.user', username=user.username))
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.username.data = user.username
    form.email.data = user.email
    form.role.data = user.role
    form.confirmed.data = user.confirmed

    return render_template('edit-profile.html', form=form, user=user)

@main.route('/edit-profile/userlist', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin_list():
    users = User.query.order_by(db.desc(User.id))

    return render_template('userlist.html', users=users)

@main.route('/drops/<page>')
def drops(page):
    user = User.query.filter_by(page=page).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
