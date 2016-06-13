# coding=utf-8
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from flask.ext.script import Shell, Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Post, Comment, Role, Follow, Permission


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Role=Role,
                Follow=Follow, Comment=Comment, Permission=Permission)
manager.add_command("Shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_CONFIG'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspaht(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """运行部署任务"""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # 把数据库迁移到最新修订版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    # 让所有用户关注自己
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()
