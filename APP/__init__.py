from flask import Flask

from APP.ext import init_ext
from APP.setting import envs
from APP.view import init_view


def creat_app(env):
    app = Flask(__name__)
    # #连接数据库URL写法：数据库名+驱动://用户名:密码@主机:端口/具体的库
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(envs.get(env))
    init_ext(app)
    init_view(app)
    return app
