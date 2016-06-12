# coding=utf-8
from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, Length, Regexp, Required
from wtforms import ValidationError
from ..models import User


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class LoginForm(Form):
    email = StringField('用户名', validators=[
        Required(message='不能为空'), Length(1, 64),
        Email()
    ])
    password = PasswordField('密码', validators=[
        Required(message='不能为空')
    ])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegistrationForm(Form):
    email = StringField('电子邮箱', validators=[
        Required(message='不能为空'), Length(1, 64),
        Email()
    ])
    username = StringField('用户名', validators=[
        Required(message='不能为空'), Length(1, 64),
        Regexp(u'^[A-Za-z][A-Za-z0-9_.]*|'
               u'[A-Za-z]*[\u4e00-\u9fa5]+[A-Za-z0-9_.]*$',
               0,
               '用户名必须只有字母，数字，'
               '点，下划线和中文')
    ])
    password = PasswordField('密码', validators=[
        Required(message='不能为空'),
        EqualTo('password2', message='两次密码必须相同')
    ])
    password2 = PasswordField('验证密码', validators=[
        Required(message='不能为空')
    ])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('此用户名已存在')


class ChangePasswordForm(Form):
    old_password = PasswordField('原密码', validators=[
        Required(message='不能为空')
    ])
    password = PasswordField('新密码', validators=[
        Required(message='不能为空'),
        EqualTo('password2', message='两次密码必须相同')
    ])
    password2 = PasswordField('验证密码', validators=[
        Required(message='不能为空')
    ])
    submit = SubmitField('修改密码')


class PasswordResetRequestForm(Form):
    email = StringField('电子邮箱', validators=[
        Required(message='不能为空'), Length(1, 64),
        Email()
    ])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('电子邮箱不存在。')


class PasswordResetForm(Form):
    email = StringField('电子邮箱', validators=[
        Required(message='不能为空'), Length(1, 64),
        Email()
    ])
    password = PasswordField('新密码', validators=[
        Required(message='不能为空'),
        EqualTo('password2', message='两次密码必须相同')
    ])
    password2 = PasswordField('验证密码', validators=[
        Required(message='不能为空')
    ])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('电子邮箱不存在。')


class ChangeEmailForm(Form):
    email = StringField('新电子邮箱', validators=[
        Required(message='不能为空'), Length(1, 64),
        Email()
    ])
    password = PasswordField('密码', validators=[
        Required(message='不能为空')
    ])
    submit = SubmitField('更改电子邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该电子邮箱已注册。')




