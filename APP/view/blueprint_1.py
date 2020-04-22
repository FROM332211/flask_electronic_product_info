from flask import Blueprint, redirect, url_for, abort, request, render_template, Response, session, flash
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from APP.ext import db
from APP.model import User, commodity_review_info, commodity_price_info
from APP.model import commodity_base_info
from APP.spider.commodity_info_spider import base_infoz
from APP.spider.tb_search_spider import taobao_spider
from APP.spider.zhihu_spider import zhihu_review_spider

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


@first.route('/index/', methods=['GET', 'POST'])
def index():
    commodity = commodity_base_info()
    commodity_list = []
    for info in commodity.query.limit(3):
        info = vars(info)
        # print(info)
        commodity_type = info.pop('commodity_type')
        name = info.pop('commodity_name')
        price = info.pop('commodity_base_price')
        img_path = info.pop('img_path')
        infos = info.pop('info').replace('>', '').split(';')
        # print(img_path)
        base_info = {}
        for i in infos:
            i = i.split(':')
            print(i)
            if len(i) == 2 and i[0] in ['后置摄像头', 'CPU型号', 'RAM容量']:
                base_info[i[0]] = i[1].replace(',', ';')
        info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
                'base_info': base_info}
        print(info['img_path'])
        commodity_list.append(info)

    return render_template('index.html', index_list=commodity_list)


@first.route('/<string:commodity_type>/<string:commodity_name>/')
def commodity_data(commodity_type, commodity_name):
    commodity = commodity_base_info()
    commodity_review = commodity_review_info()
    commodity_price = commodity_price_info
    price_list = []
    review_list = []
    # print(commodity_name)
    # print(commodity_type)
    res = commodity.query.all()
    # print(vars(res[0]))
    phone_list = []
    for i in res:
        phone_list.append(i.commodity_name)
    # print(res)
    info = commodity.query.filter(commodity_base_info.commodity_type == commodity_type,
                                  commodity_base_info.commodity_name == commodity_name).all()
    info_list = []
    # print(info)
    info = info[0]
    info = vars(info)
    commodity_type = info.pop('commodity_type')
    name = info.pop('commodity_name')
    price = info.pop('commodity_base_price')
    img_path = info.pop('img_path')
    base_info = {}
    infos = info.pop('info').replace('>', '').split(';')
    for i in infos:
        i = i.split(':')
        # print(i)
        if len(i) >= 2:
            info_list.append(i[0])
        if len(i) >= 2 and i[0] in ['后置摄像头', 'CPU型号', 'RAM容量']:
            base_info[i[0]] = i[1].replace(',', ';')
    info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
            'base_info': base_info, 'phone_list': phone_list, 'info_list': info_list}

    price_infos = commodity_price.query.filter(commodity_price_info.commodity_type == commodity_type,
                                               commodity_price_info.commodity_name == commodity_name).order_by(
        -commodity_price_info.price).all()
    for price_info in price_infos:
        price_list.append({'price': price_info.price,
                           'price_title': price_info.price_title,
                           'price_url': price_info.price_url,
                           'price_img_path': price_info.price_img_path})

    review_infos = commodity_review.query.filter(commodity_review_info.commodity_type == commodity_type,
                                                 commodity_review_info.commodity_name == commodity_name).all()
    for review_info in review_infos:
        review_list.append({'review_url': review_info.review_url,
                            'review_title': review_info.review_title.replace('<em>', '').replace('</em>', ''),
                            'review_img_path': review_info.review_img_path,
                            'review_excerpt': review_info.review_excerpt.replace('<em>', '').replace('</em>', '')})
    return render_template('commodity_data.html', commodity_type=commodity_type, commodity_name=commodity_name,
                           info=info, price_list=price_list, review_list=review_list)


@first.route('/index/<string:commodity_type>/<string:commodity_brand>/')
def commodity_brand(commodity_type, commodity_brand):
    commodity = commodity_base_info()
    res = commodity.query.filter(commodity_base_info.commodity_type == commodity_type,
                                 commodity_base_info.commodity_brand == commodity_brand).all()
    return 'hello'


@first.route('/contrast')
def Contrast():
    commodity_type = request.args.get('commodity_type')
    commodity_name = request.args.get('commodity_name')
    commodity_contrast_name = request.args.get('commodity_contrast_name')
    contrast_info = request.args.get('contrast_info').split(',')
    # print(commodity_type)
    # print(commodity_name)
    print(contrast_info)
    # return commodity_type+';'+commodity_name
    commodity = commodity_base_info()
    commodity_review = commodity_review_info()
    commodity_price = commodity_price_info
    price_list = []
    review_list = []
    # print(commodity_name)
    # print(commodity_type)
    res = commodity.query.all()
    # print(vars(res[0]))
    phone_list = []
    for i in res:
        phone_list.append(i.commodity_name)
    # print(res)
    info = commodity.query.filter(commodity_base_info.commodity_type == commodity_type,
                                        commodity_base_info.commodity_name == commodity_name).all()
    info_list = []
    print(info)
    info = info[0]
    info = vars(info)
    commodity_type = info.pop('commodity_type')
    name = info.pop('commodity_name')
    price = info.pop('commodity_base_price')
    img_path = info.pop('img_path')
    base_info = {}
    infos = info.pop('info').replace('>', '').split(';')
    for i in infos:
        i = i.split(':')
        # print(i)
        if len(i) >= 2:
            info_list.append(i[0])
            text = ''
            texts = i[1].split(',')[:-2]
        if len(i) >= 2 and i[0] in contrast_info:
            # print(type(text))
            # print(text)
            for c in texts:
                text += c+';'
            base_info[i[0]] = text
    info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
            'base_info': base_info, 'phone_list': phone_list, 'info_list': info_list}

    price_infos = commodity_price.query.filter(commodity_price_info.commodity_type == commodity_type,
                                               commodity_price_info.commodity_name == commodity_name).order_by(
        -commodity_price_info.price).all()
    for price_info in price_infos:
        price_list.append({'price': price_info.price,
                           'price_title': price_info.price_title,
                           'price_url': price_info.price_url,
                           'price_img_path': price_info.price_img_path})

    review_infos = commodity_review.query.filter(commodity_review_info.commodity_type == commodity_type,
                                                 commodity_review_info.commodity_name == commodity_name).all()
    for review_info in review_infos:
        review_list.append({'review_url': review_info.review_url,
                            'review_title': review_info.review_title.replace('<em>', '').replace('</em>', ''),
                            'review_img_path': review_info.review_img_path,
                            'review_excerpt': review_info.review_excerpt.replace('<em>', '').replace('</em>', '')})
    return render_template('commodity_contrast.html', commodity_type=commodity_type, commodity_name=commodity_name,
                           info=info, price_list=price_list, review_list=review_list)


@first.route('/init_base_info/')
def aa():
    base_infoz()
    return 'sussce'


@first.route('/init_price_info/')
def taobao():
    taobao_spider()
    return 'sussce'


@first.route('/init_review_info/')
def zhihu():
    zhihu_review_spider()
    return 'sussce'
