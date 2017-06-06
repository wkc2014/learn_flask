from app.decorators import admin_required
from . import main, Permission
from .forms import EditPofileForm, EditPofileFormAdmin, PostForm, AddArticleForm, ArticleForm
from flask import render_template, abort, redirect, url_for, flash, request, current_app
from app.models import User, db, Role, Drops, Post, Article
from flask_login import current_user, login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    articles = Article.query.order_by(Article.create_time.desc()).limit(10)
    return render_template('index.html', form=form, posts=articles)


@main.route('/articles', methods=['GET', 'POST'])
def articles():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('article.html', posts=posts, pagination=pagination)


@main.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get_or_404(id)
    article.add_view(article, db)
    return render_template('view-article.html', post=article)


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


@main.route('/drops', methods=['GET', 'POST'])
@login_required
def drops():
    page = request.args.get('page', default=1, type=int)
    pagination = Drops.query.order_by(Drops.id).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    d_posts = pagination.items

    return render_template('drops.html', posts=d_posts, pagination=pagination)


@main.route('/<drops_name>', methods=['GET', 'POST'])
@login_required
def per_drops(drops_name):
    return render_template(drops_name)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated')
        db.session.commit()
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/about', methods=['GET', 'POST'])
def about():
    form = ArticleForm()
    id = 1
    post = Article.query.get_or_404(id)
    post.add_view(post, db)
    return render_template('about.html', posts=post, form=form)


@main.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.add(article)
        flash('The post has been updated')
        db.session.commit()
        return redirect(url_for('.article', id=article.id))
    form.title.data = article.title
    form.content.data = article.content
    return render_template('edit_post.html', form=form, posts=article)


@main.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    if not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = AddArticleForm()
    article = Article()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.add(article)
        flash('The article has been updated')
        db.session.commit()
        return redirect(url_for('.article', id=article.id))
    # form.content.data = article.content
    return render_template('add_article.html', form=form, posts=article)
