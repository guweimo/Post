# coding=utf-8
import os
from flask import flash, render_template, redirect, url_for, request, abort,\
    current_app, make_response, jsonify
from .forms import EditAdminProfileForm, EditProfileForm, PostForm,\
    CommentForm, SearchForm
from flask.ext.login import current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from ..models import User, Role, Permission, Post, Comment, \
    Assortment, Follow
from .. import db
from ..decorators import permission_required, admin_required
from . import main
from werkzeug.utils import secure_filename


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           show_followed=show_followed, pagination=pagination,
                           endpoint='.index')


@main.route('/category/<int:id>')
def category(id):
    page = request.args.get('page', 1, type=int)
    category_follow = False
    is_category = True
    if current_user.is_authenticated:
        category_follow = bool(request.cookies.get('category_follow', ''))
    if category_follow:
        query = Assortment.query.get_or_404(id).posts.join(Follow, Follow.followed_id == Post.author_id) \
                .filter(Follow.follower_id == current_user.id)
    else:
        query = Assortment.query.get_or_404(id).posts
    pagination = query.order_by(Post.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, is_category=is_category,
                           category_follow=category_follow, pagination=pagination,
                           id=id, endpoint='.index')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('你的个人信息修改成功')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditAdminProfileForm(user=user, current_user=current_user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.confirmed = form.confirmed.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('此用户的信息修改成功')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.confirmed.data = user.confirmed
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/publish_post', methods=['GET', 'POST'])
def publish_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(subject=form.subject.data,
                    body=form.body.data,
                    assortment=Assortment.query.get(form.assortment.data),
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('发布文章成功。')
        return redirect(url_for('.post', id=post.id))
    return render_template('publish_post.html', form=form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('评论成功。')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('.search_body', body=form.body.data))
    return render_template('search.html', form=form)


@main.route('/search_body/<string:body>', methods=['GET', 'POST'])
def search_body(body):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('.search_body', body=form.body.data))
    page = request.args.get('page', 1, type=int)
    if body is None and body == '':
        pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    else:
        pagination = Post.query.filter(Post.subject.ilike('%' + body + '%')).order_by(
            Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('search.html', form=form,
                           pagination=pagination, posts=posts)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.subject = form.subject.data
        post.body = form.body.data
        post.assortment = Assortment.query.get(form.assortment.data)
        db.session.add(post)
        db.session.commit()
        flash('你的文章修改成功。')
        return redirect(url_for('.post', id=post.id, page=-1))
    form.subject.data = post.subject
    form.body.data = post.body
    form.assortment.data = post.assortment_id
    return render_template('edit_post.html', form=form)


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'jpe', 'ico', 'svg', 'svgz', 'tiff', 'tif', 'psp', 'psd'}
UPLOAD_FOLDER = '/static/avatar/'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/edit_avatar', methods=['GET', 'POST'])
@login_required
def edit_avatar():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            url = os.path.join('app' + UPLOAD_FOLDER, filename)
            file.save(url)
            current_user.avatar_hash = UPLOAD_FOLDER + filename
            db.session.add(current_user)
            db.session.commit()
        return redirect(url_for('.user', username=current_user.username))
    return render_template('edit_avatar.html')


@main.route('/follow/<int:id>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    user = User.query.get_or_404(id)
    bol = False
    if user is None:
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        current_user.unfollow(user)
        bol = False
    elif not current_user.is_following(user):
        current_user.follow(user)
        bol = True
    count = user.followers.count() - 1
    return jsonify(bol=bol, count=count)


'''@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('你没有关注此用户')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('你取消关注了%s' % user.username)
    return redirect(url_for('.user', username=username))'''


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = ({'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items)
    return render_template('followers.html', user=user, title='关注了',
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('无效的用户')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = ({'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items)
    return render_template('followers.html', user=user, title='关注者',
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/category_all/<int:id>')
def show_category_all(id):
    resp = make_response(redirect(url_for('.category', id=id)))
    resp.set_cookie('category_follow', '', max_age=30*24*60*60)
    return resp


@main.route('/category_followed/<int:id>')
@login_required
def show_category_followed(id):
    resp = make_response(redirect(url_for('.category', id=id)))
    resp.set_cookie('category_follow', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/edit_comment/<int:id>')
@login_required
def edit_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user.comments.id != comment.id:
        flash('你不是原作者')
        return redirect(url_for('.index'))
    form = Comment()
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.add(comment)
        db.session.commit()
        flash('修改成功')
        return redirect('.post', id=comment.posts.id)
    return render_template('edit_comment.html', form=form,
                           comment=comment)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/disables')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def disables():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(disabled=True).\
        order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
