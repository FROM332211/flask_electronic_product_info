from flask import Blueprint, redirect, url_for, abort, request, render_template, Response, session, flash
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from APP.ext import db
from APP.model import User
from APP.model import commodity_info

first = Blueprint('first', __name__)


@first.route('/')
def hello():
    return 'first blue'


@first.route('/create_db')
def create_db():
    db.create_all()
    return '创建成功'


@first.route('/adduser')
def adduser():
    user = User()
    user.username = 'Tom'
    user.password = '123456'
    user.save()
    return '添加成功'


@first.route('/drop_db')
def drop_db():
    db.drop_all()
    return '删除成功'


@first.route('/get_id/<string:id>/<string:id1>/')
def get_id(id, id1):
    return '{}{}'.format(id, id1)


@first.route('/redirect/<int:id>')
def redir(id):
    return redirect(url_for('first.get_id', id=id))


@first.route('/error/')
def go_error():
    abort(401)
    return 404


@first.errorhandler(401)
def error(er):
    return '捕获401'


@first.route('/mine/')
def mine():
    # return 'Hello,%s' % request.cookies.get('username')
    return 'Hello,%s' % session['username']


class password_form(FlaskForm):
    user = StringField('账号',
                       validators=[Length(min=6, max=12, message='用户名长度为6~12位'), DataRequired(message='请输入用户名密码')])
    submit = SubmitField('提交')


@first.route('/index/', methods=['GET', 'POST'])
def index():
    commodity = commodity_info()
    index_list = []
    for info in commodity.query.limit(3):
        info = vars(info)
        info.pop('_sa_instance_state')
        info.pop('id')
        commodity_type = info.pop('commodity_type')
        name = info.pop('name')
        price = info.pop('price')
        img_path = info.pop('img_path')
        for i in info.keys():
            if info[i]:
                pass
            else:
                info.pop[i]
        base_info = info
        info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
                'base_info': base_info}
        index_list.append(info)
    return render_template('index.html', index_list=index_list)


@first.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = User()
        username = request.form.get('username')
        password = request.form.get('password')
        if user.query.filter_by(username=username, password=password).first():
            session['username'] = request.form.get('username')
            return redirect(url_for('first.index'))
            # response.set_cookie('username', request.form.get('username'))
        else:
            flash('账号或密码错误')
            return render_template('login.html')


@first.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        response = Response(render_template('register.html'))
        return response
    else:
        user = User()
        username = request.form.get('username')
        password = request.form.get('password')
        # print(user.query.filter_by(username=username).first())
        if user.query.filter_by(username=username).first():
            flash('账号已存在')
            return render_template('register.html')
        else:
            user.username = username
            user.password = password
            user.save()
            return redirect(url_for('first.login'))


@first.route('/logout/', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('first.index'))


@first.route('/<string:commodity_type>/<string:commodity_name>/')
def commodity_data(commodity_type, commodity_name):
    commodity = commodity_info()
    print(commodity_name)
    print(commodity_type)
    res = commodity.query.filter(commodity_info.commodity_type == commodity_type, commodity_info.name != commodity_name).all()
    print(res)
    info = commodity.query.filter(commodity_info.commodity_type == commodity_type, commodity_info.name == commodity_name).all()
    select_list = []
    print(info)
    info = vars(info[0])
    print(info)
    info.pop('_sa_instance_state')
    info.pop('id')
    commodity_type = info.pop('commodity_type')
    name = info.pop('name')
    price = info.pop('price')
    img_path = info.pop('img_path')
    for i in info.keys():
        if info[i]:
            pass
        else:
            info.pop[i]
    base_info = info
    for i in res:
        select_list.append(i.name)
    info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
            'base_info': base_info, 'select_list': select_list}
    return render_template('commodity_data.html', commodity_type=commodity_type, commodity_name=commodity_name,
                           info=info)
