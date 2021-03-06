# coding=utf-8
from flask import render_template, redirect, url_for, flash, request, \
    jsonify, json
from flask.ext.login import login_user, login_required, logout_user, \
    current_user
from . import auth
from ..models import User
from .. import db
from ..email import send_email
from .forms import ChangePasswordForm, PasswordResetForm, LoginForm, \
    PasswordResetRequestForm, RegistrationForm, ChangeEmailForm

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的密码或用户名')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    username=form.username.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的账号',
                   'auth/email/confirm', user=user, token=token)
        flash('确认邮件已经发送到你的电子邮箱中。')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/check_username', methods=['POST'])
def check_username():
    username = request.form['username']
    if User.query.filter_by(username=username).first():
        return jsonify(result='该用户名已存在')
    else:
        return jsonify(result='')


@auth.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['email']
    if User.query.filter_by(email=email).first():
        return jsonify(result='该电子邮件已存在')
    else:
        return jsonify(result='')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经确认您的帐户。谢谢!')
    else:
        flash('确认链接无效或已过期。')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账号',
               'auth/email/confirm', user=current_user, token=token)
    flash('确认邮件已经发送到你的电子邮箱中。')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('你的密码已经更新。请重新登陆~')
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash('无效的密码')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置你的密码',
                       'auth/email/reset_password', user=user, token=token)
        flash('一封重置你的密码的电子邮件发送了给你。')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('你的密码已经更新')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '确认你的电子邮箱',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('电子邮件指示来确认你的新电子邮件地址已经发送给你。')
            return redirect(url_for('main.index'))
        else:
            flash('无效的密码或电子邮箱')
        return redirect(url_for('main.index'))
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('你的电子邮件已更改。')
    else:
        flash('无效的请求。')
    return redirect(url_for('main.index'))

