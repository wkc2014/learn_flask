# -*- coding:utf-8 -*-
from app.decorators import admin_required
from . import main, Permission
from .forms import AddArticleForm, ArticleForm, ArticleFormView  # ,PostForm , EditPofileForm, EditPofileFormAdmin
from flask import render_template, abort, redirect, url_for, flash, request, current_app
from app.models import User, db, Role, Drops, Post, Article
from flask_login import current_user, login_required
import time


@main.route('/', methods=['GET', 'POST'])
def index():
    articles = Article.query.order_by(Article.create_time.desc()).limit(10)
    return render_template('index.html', posts=articles)


@main.route('/list', methods=['GET', 'POST'])
def article_list():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('article_list.html', posts=posts, pagination=pagination)


@main.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get_or_404(id)
    article.add_view(article, db)
    return render_template('article_view.html', post=article)


@main.route('/drops/', methods=['GET', 'POST'])
@login_required
def drops_list():
    page = request.args.get('page', default=1, type=int)
    pagination = Drops.query.order_by(Drops.id).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    d_posts = pagination.items

    return render_template('drops.html', posts=d_posts, pagination=pagination)


@main.route('/<drops_name>', methods=['GET', 'POST'])
@login_required
def drops(drops_name):
    drops = Drops.query.get_or_404(drops_name)
    return render_template(drops.path)


@main.route('/about', methods=['GET', 'POST'])
def about():
    id = 1
    post = Article.query.get_or_404(id)
    post.add_view(post, db)
    return render_template('about.html', posts=post)


@main.route('/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    article = Article.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = ArticleForm()
    view_form = ArticleFormView()

    if request.form.get('submit', None) == u"保存":
        article.title = form.title.data
        article.content = form.content.data
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('.article', id=article.id))
    elif request.form.get('publish_view', None) == u"预览":
        view_form.title.data = form.title.data
        view_form.content.data = form.content.data
        return render_template('admin/publish_view.html', form=view_form)

    # 这里的赋值不能再submit之前，这样会导致不能更新数据
    form.title.data = article.title
    form.content.data = article.content
    return render_template('admin/article_edit.html', form=form)


@main.route('/article/publish', methods=['GET', 'POST'])
@login_required
def publish():
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = AddArticleForm()
    view_form = ArticleFormView()
    article = Article()

    if request.form.get('submit', None) == u"保存":
        article.title = form.title.data
        article.content = form.content.data
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('.article', id=article.id))
    elif request.form.get('publish_view', None) == u"预览":
        view_form.title.data = form.title.data
        view_form.content.data = form.content.data
        return render_template('admin/publish_view.html', form=view_form)

    return render_template('admin/publish.html', form=form)


@main.route('/article/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def article_del(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    flash('Delete Successful')
    db.session.commit()
    return redirect(url_for('.article_list'))

# @main.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         abort(404)
#     posts = user.posts.order_by(Post.timestamp.desc()).all()
#     return render_template('user.html', user=user, posts=posts)


# @main.route('/edit-profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditPofileForm()
#     if form.validate_on_submit():
#         current_user.name = form.name.data
#         current_user.location = form.location.data
#         current_user.about_me = form.about_me.data
#         db.session.add(current_user)
#         flash('You profile has been update')
#         db.session.commit()
#         return redirect(url_for('main.user', username=current_user.username))
#     form.name.data = current_user.name
#     form.location.data = current_user.location
#     form.about_me.data = current_user.about_me
#
#     return render_template('edit_profile.html', form=form)


# @main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_profile_admin(id):
#     user = User.query.get_or_404(id)
#     form = EditPofileFormAdmin(user=user)
#     if form.validate_on_submit():
#         user.name = form.name.data
#         user.location = form.location.data
#         user.about_me = form.about_me.data
#         user.username = form.username.data
#         user.email = form.email.data
#         user.role = Role.query.get(form.role.data)
#         user.confirmed = form.confirmed.data
#         db.session.add(user)
#         flash('You profile has been update')
#         db.session.commit()
#         return redirect(url_for('main.user', username=user.username))
#     form.name.data = user.name
#     form.location.data = user.location
#     form.about_me.data = user.about_me
#     form.username.data = user.username
#     form.email.data = user.email
#     form.role.data = user.role
#     form.confirmed.data = user.confirmed
#
#     return render_template('edit_profile.html', form=form, user=user)


# @main.route('/edit-profile/userlist', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_profile_admin_list():
#     users = User.query.order_by(db.desc(User.id))
#     return render_template('userlist.html', users=users)
