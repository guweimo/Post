# coding=utf-8
from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, SubmitField, SelectField, \
    TextAreaField
from wtforms.validators import Email, Regexp, Required, Length
from wtforms import ValidationError
from ..models import User, Role


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class NameForm(Form):
    name = StringField('称呼', validators=[
        Required(message='不能为空'), Length(0, 64)
    ])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')


class EditAdminProfileForm(Form):
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
               '点和下划线')
    ])
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditAdminProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('该电子邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and\
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在')


class PostForm(Form):
    subject = StringField('标题', validators=[
        Required(message='不能为空'),
        Length(1, 256)
    ])
    body = TextAreaField('内容', validators=[
        Required(message='不能为空')
    ])
    submit = SubmitField('提交')


class CommentForm(Form):
    body = TextAreaField('评论', validators=[
        Required(message='不能为空')
    ])
    submit = SubmitField('提交')


class SearchForm(Form):
    body = StringField()
    submit = SubmitField('搜索')
