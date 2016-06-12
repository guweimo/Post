# coding=utf-8
import unittest, re
from app import create_app, db
from app.models import User, Role
from flask import url_for


class MxtanClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_role()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('游客' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # 注册账号
        response = self.client.get(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': u'谷维陌',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertTrue(response.status_code == 302)

        # 使用新注册账号登录
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('你好，\s+谷维陌', data))
        self.assertTrue('你还没有确认您的帐户' in data)

        # 发送确认令牌
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('你已经确认您的帐户' in data)

        # 退出
        response = self.client.post(url_for('auth.logout'),
                                    follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('退出登录' in data)

