from app.decorators import admin_required
from . import main, Permission
from .forms import EditPofileForm, EditPofileFormAdmin, PostForm
from flask import render_template, abort, redirect, url_for, flash, request, current_app
from app.models import User, db, Role, Drops, Post
from flask_login import current_user, login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items

    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))

    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/article', methods=['GET', 'POST'])
def article():
    return render_template('article.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


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


@main.route('/drops/page/<page>', methods=['GET', 'POST'])
def drops(page):
    pagination = Drops.query.order_by(Drops.id.desc()).paginate(page, 20, False)
    posts = pagination.items
    if article is None:
        abort(404)
    return render_template('drops.html', posts=posts, pagination=pagination)
