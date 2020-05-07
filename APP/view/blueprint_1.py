import re

from flask import Blueprint, redirect, url_for, abort, request, render_template, Response, session, flash
from flask_wtf import FlaskForm
from sqlalchemy import and_, or_
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from APP.ext import db
from APP.model import User, commodity_review_info, commodity_price_info, user_collection
from APP.model import commodity_base_info
from APP.spider.commodity_info_spider import base_infoz
from APP.spider.tb_search_spider import taobao_spider
from APP.spider.zhihu_spider import zhihu_review_spider

first = Blueprint('first', __name__)


@first.route('/')
def hello():
    return redirect(url_for('first.index'))
#
#
# @first.route('/create_db')
# def create_db():
#     db.create_all()
#     return '创建成功'
#
#
# @first.route('/adduser')
# def adduser():
#     user = User()
#     user.username = 'Tom'
#     user.password = '123456'
#     user.save()
#     return '添加成功'
#
#
# @first.route('/drop_db')
# def drop_db():
#     db.drop_all()
#     return '删除成功'
#
#
# @first.route('/get_id/<string:id>/<string:id1>/')
# def get_id(id, id1):
#     return '{}{}'.format(id, id1)
#
#
# @first.route('/redirect/<int:id>')
# def redir(id):
#     return redirect(url_for('first.get_id', id=id))
#
#
# @first.route('/error/')
# def go_error():
#     abort(401)
#     return 404
#
#
# @first.errorhandler(401)
# def error(er):
#     return '捕获401'
#
#
# @first.route('/mine/')
# def mine():
#     # return 'Hello,%s' % request.cookies.get('username')
#     return 'Hello,%s' % session['username']
#
#
# class password_form(FlaskForm):
#     user = StringField('账号',
#                        validators=[Length(min=6, max=12, message='用户名长度为6~12位'), DataRequired(message='请输入用户名密码')])
#     submit = SubmitField('提交')


@first.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user = User()
        username = request.form.get('username')
        password = request.form.get('password')
        if len(user.query.filter_by(username=username, password=password).all()) > 0:
            session['username'] = username
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
        email = request.form.get('email')
        if username and password and email:
            if len(re.findall(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email)) < 1:
                flash('邮箱格式错误，请重试')
                return render_template('register.html')
            if len(user.query.filter_by(username=username).all()) > 0:
                flash('账号已存在')
                return render_template('register.html')
            else:
                user.username = username
                user.password = password
                user.email = email
                user.save()
                return redirect(url_for('first.login'))
        else:
            flash('账号、密码或邮箱为空')
            return render_template('register.html')


@first.route('/logout/', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('first.index'))


@first.route('/modify_password/', methods=['GET', 'POST'])
def modify_password():
    if request.method == 'GET':
        return render_template('modify_password.html')
    else:
        username = session['username']
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        user = User()
        now_user = user.query.filter(User.username == username).all()[0]
        if now_user.password == old_password:
            now_user.password = new_password
            db.session.commit()
            flash('修改密码成功')
            return render_template('modify_password.html')
        else:
            flash('原密码错误，请重试')
            return render_template('modify_password.html')


@first.route('/index/')
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
        n = 0
        for i in infos:
            if n > 3:
                break
            n += 1
            # print(i)
            i = i.split(':')
            if len(i) < 2:
                continue
            # print(i[1])
            text = ''
            texts = i[1].split(',')
            if len(texts) >= 3:
                texts = texts[:-2]
            # print(texts)
            # print(type(text))
            # print(text)
            for c in texts:
                if c != '':
                    text += c + ';'
            base_info[i[0]] = text.replace('，;', '')
        info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
                'base_info': base_info}
        # print(info['img_path'])
        commodity_list.append(info)

    return render_template('index.html', index_list=commodity_list)


@first.route('/<string:commodity_type>/<string:commodity_name>/')
def commodity_data(commodity_type, commodity_name):
    commodity = commodity_base_info()
    commodity_review = commodity_review_info()
    commodity_price = commodity_price_info()
    user = User()
    user_collect = user_collection()
    price_list = []
    review_list = []
    # print(commodity_name)
    # print(commodity_type)
    res = commodity.query.filter(commodity_base_info.commodity_type == commodity_type).all()
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
    infos = info.pop('info')
    infos = re.sub(r'(击败.*?)，', '', infos)
    infos = infos.replace('>', '').split(';')
    n = 0
    for i in infos:
        i = i.split(':')
        if len(i) < 2:
            continue
        info_list.append(i[0])
    for i in infos:
        if n > 3:
            break
        n += 1
        # print(i)
        i = i.split(':')
        if len(i) < 2:
            continue
        # print(i[1])
        text = ''
        texts = i[1].split(',')
        if len(texts) >= 3:
            texts = texts[:-2]
        # print(texts)
        # print(type(text))
        # print(text)
        for c in texts:
            if c != '':
                text += c + ';'
        base_info[i[0]] = text.replace('，;', '')
    info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
            'base_info': base_info, 'phone_list': phone_list, 'info_list': info_list}
    # print(session['username'])
    if 'username' in session:
        user_id = user.query.filter(User.username == session['username']).all()[0].user_id
        # print(user_id)
        # print(vars(user_collection.query.all()[0]))
        # price_infos = commodity_price.query(commodity_price_info,user_collection).outerjoin(user_collection, commodity_price_info.id == user_collection.commodity_info_id and user_collection.user_id == user_id).filter(commodity_price_info.commodity_type == commodity_type,commodity_price_info.commodity_name == commodity_name).order_by(-commodity_price_info.price).all()
        price_collection = db.session.query(commodity_price_info, user_collection).outerjoin(user_collection, commodity_price_info.id == user_collection.commodity_info_id).filter(commodity_price_info.commodity_type == commodity_type,commodity_price_info.commodity_name == commodity_name, user_collection.user_id == user_id).order_by(-commodity_price_info.price).all()
        collection_priceid_list = []
        for collection in price_collection:
            collection_priceid_list.append(collection[0].id)
        price_infos = commodity_price.query.filter(commodity_price_info.commodity_type == commodity_type,
                                                   commodity_price_info.commodity_name == commodity_name
                                                   ).order_by(-commodity_price_info.price).all()
        price_id = 0
        # print(price_infos)
        for price_info in price_infos:
            # print(vars(price_info[0]))
            # print(vars(price_info[1]))
            price_id += 1
            if price_info.id in collection_priceid_list:
                price_list.append({'price': price_info.price,
                                   'price_title': price_info.price_title,
                                   'price_url': price_info.price_url,
                                   'price_img_path': price_info.price_img_path,
                                   'price_id': price_info.id,
                                   'collection_flag': 1})
            else:
                price_list.append({'price': price_info.price,
                                   'price_title': price_info.price_title,
                                   'price_url': price_info.price_url,
                                   'price_img_path': price_info.price_img_path,
                                   'price_id': price_info.id,
                                   'collection_flag': 0})
    else:
        price_infos = commodity_price.query.filter(commodity_price_info.commodity_type == commodity_type,
                                                   commodity_price_info.commodity_name == commodity_name).order_by(-commodity_price_info.price).all()
        price_id = 0
        for price_info in price_infos:
            price_id += 1
            price_list.append({'price': price_info.price,
                               'price_title': price_info.price_title,
                               'price_url': price_info.price_url,
                               'price_img_path': price_info.price_img_path,
                               'price_id': price_info.id,
                               'collection_flag': 0})

    review_infos = commodity_review.query.filter(commodity_review_info.commodity_type == commodity_type,
                                                 commodity_review_info.commodity_name == commodity_name).all()
    for review_info in review_infos:
        review_list.append({'review_url': review_info.review_url,
                            'review_title': review_info.review_title.replace('<em>', '').replace('</em>', ''),
                            'review_img_path': review_info.review_img_path,
                            'review_excerpt': review_info.review_excerpt.replace('<em>', '').replace('</em>', '')})
    return render_template('commodity_data.html', commodity_type=commodity_type, commodity_name=commodity_name,
                           info=info, price_list=price_list, review_list=review_list)


@first.route('/index/<string:commodity_type>/<string:commodity_brand>/', methods=['GET', 'POST'])
def commodity_brand(commodity_type, commodity_brand):
    commodity = commodity_base_info()
    path_list = []
    commodity_list = []
    if request.method == 'POST':
        key_word = request.form.get('search_keyword')
        res = commodity.query.filter(or_(commodity_base_info.commodity_type.contains(key_word),
                                         commodity_base_info.commodity_brand.contains(key_word),
                                         commodity_base_info.commodity_name.contains(key_word))).all()
        path_list.append('搜索')
        path_list.append(key_word)
    else:
        if commodity_brand == '*':
            res = commodity.query.filter(commodity_base_info.commodity_type == commodity_type).all()
            path_list.append(commodity_type)
        else:
            res = commodity.query.filter(commodity_base_info.commodity_type == commodity_type,
                                         commodity_base_info.commodity_brand == commodity_brand).all()
            path_list.append(commodity_type)
            path_list.append(commodity_brand)

    commodity_sum = len(res)

    for info in res:
        info = vars(info)
        # print(info)
        commodity_type = info.pop('commodity_type')
        name = info.pop('commodity_name')
        price = info.pop('commodity_base_price')
        img_path = info.pop('img_path')
        infos = info.pop('info').replace('>', '').split(';')
        # print(img_path)
        base_info = {}
        n = 0
        for i in infos:
            if n > 3:
                break
            n += 1
            # print(i)
            i = i.split(':')
            if len(i) < 2:
                continue
            # print(i[1])
            text = ''
            texts = i[1].split(',')
            if len(texts) >= 3:
                texts = texts[:-2]
            # print(texts)
            # print(type(text))
            # print(text)
            for c in texts:
                if c != '':
                    text += c + ';'
            base_info[i[0]] = text.replace('，;', '')
        info = {'name': name, 'price': price, 'img_path': img_path, 'commodity_type': commodity_type,
                'base_info': base_info}
        # print(info['img_path'])
        commodity_list.append(info)

    return render_template('commodity_brand.html', index_list=commodity_list, path=path_list,
                           commodity_sum=commodity_sum)


@first.route('/contrast')
def Contrast():
    commodity_type = request.args.get('commodity_type')
    commodity_name = request.args.get('commodity_name')
    commodity_contrast_name = request.args.get('commodity_contrast_name')
    contrast_info = request.args.get('contrast_info').split(',')
    # print(commodity_type)
    # print(commodity_name)
    # print(contrast_info)
    # return commodity_type+';'+commodity_name
    commodity = commodity_base_info()
    commodity_review = commodity_review_info()
    commodity_price = commodity_price_info()
    user = User()
    price_list = []
    review_list = []
    # print(commodity_name)
    # print(commodity_type)
    res = commodity.query.filter(commodity_base_info.commodity_type == commodity_type).all()
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
    info_commodity_type = info.pop('commodity_type')
    info_name = info.pop('commodity_name')
    info_price = info.pop('commodity_base_price')
    info_img_path = info.pop('img_path')
    base_info = {}
    infos = info.pop('info')
    infos = re.sub(r'(击败.*?)，', '', infos)
    infos = infos.replace('>', '').split(';')
    for i in infos:
        # print(i)
        i = i.split(':')
        if len(i) < 2:
            continue
        # print(i[1])
        info_list.append(i[0])
        text = ''
        texts = i[1].split(',')
        if len(texts) >= 3:
            texts = texts[:-2]
        # print(texts)
        if i[0] in contrast_info:
            # print(type(text))
            # print(text)
            for c in texts:
                if c != '':
                    text += c + ';'
            base_info[i[0]] = text.replace('，;', '')
    info = {'name': info_name, 'price': info_price, 'img_path': info_img_path, 'commodity_type': info_commodity_type,
            'base_info': base_info, 'phone_list': phone_list, 'info_list': info_list}

    other_info = commodity.query.filter(commodity_base_info.commodity_type == commodity_type,
                                        commodity_base_info.commodity_name == commodity_contrast_name).all()
    other_info = other_info[0]
    other_info_commodity_type = other_info.commodity_type
    other_info_commodity_name = other_info.commodity_name
    other_info_info = other_info.info
    other_info_img_path = other_info.img_path
    other_info_commodity_base_price = other_info.commodity_base_price
    other_infos = re.sub(r'(击败.*?)，', '', other_info_info)
    other_infos = other_infos.replace('>', '').split(';')
    other_base_info = {}
    for i in other_infos:
        # print(i)
        i = i.split(':')
        if len(i) < 2:
            continue
        # print(i[1])
        info_list.append(i[0])
        text = ''
        texts = i[1].split(',')
        if len(texts) >= 3:
            texts = texts[:-2]
        # print(texts)
        if i[0] in contrast_info:
            # print(type(text))
            # print(text)
            for c in texts:
                if c != '':
                    text += c + ';'
            other_base_info[i[0]] = text.replace('，;', '')
    other_info = {
        'name': other_info_commodity_name, 'price': other_info_commodity_base_price, 'img_path': other_info_img_path,
        'commodity_type': other_info_commodity_type, 'base_info': other_base_info
    }

    if 'username' in session:
        user_id = user.query.filter(User.username == session['username']).all()[0].user_id
        # print(user_id)
        # print(vars(user_collection.query.all()[0]))
        # price_infos = commodity_price.query(commodity_price_info,user_collection).outerjoin(user_collection, commodity_price_info.id == user_collection.commodity_info_id and user_collection.user_id == user_id).filter(commodity_price_info.commodity_type == commodity_type,commodity_price_info.commodity_name == commodity_name).order_by(-commodity_price_info.price).all()
        price_collection = db.session.query(commodity_price_info, user_collection).outerjoin(user_collection,
                                                                                             commodity_price_info.id == user_collection.commodity_info_id).filter(
            commodity_price_info.commodity_type == commodity_type,
            commodity_price_info.commodity_name == commodity_name, user_collection.user_id == user_id).order_by(
            -commodity_price_info.price).all()
        collection_priceid_list = []
        for collection in price_collection:
            collection_priceid_list.append(collection[0].id)
        price_infos = commodity_price.query.filter(commodity_price_info.commodity_type == commodity_type,
                                                   commodity_price_info.commodity_name == commodity_name
                                                   ).order_by(-commodity_price_info.price).all()
        price_id = 0
        # print(price_infos)
        for price_info in price_infos:
            # print(vars(price_info[0]))
            # print(vars(price_info[1]))
            price_id += 1
            if price_info.id in collection_priceid_list:
                price_list.append({'price': price_info.price,
                                   'price_title': price_info.price_title,
                                   'price_url': price_info.price_url,
                                   'price_img_path': price_info.price_img_path,
                                   'price_id': price_info.id,
                                   'collection_flag': 1})
            else:
                price_list.append({'price': price_info.price,
                                   'price_title': price_info.price_title,
                                   'price_url': price_info.price_url,
                                   'price_img_path': price_info.price_img_path,
                                   'price_id': price_info.id,
                                   'collection_flag': 0})
    else:
        price_infos = commodity_price.query.filter(commodity_price_info.commodity_type == commodity_type,
                                                   commodity_price_info.commodity_name == commodity_name).order_by(
            -commodity_price_info.price).all()
        price_id = 0
        for price_info in price_infos:
            price_id += 1
            price_list.append({'price': price_info.price,
                               'price_title': price_info.price_title,
                               'price_url': price_info.price_url,
                               'price_img_path': price_info.price_img_path,
                               'price_id': price_info.id,
                               'collection_flag': 0})

    review_infos = commodity_review.query.filter(commodity_review_info.commodity_type == commodity_type,
                                                 commodity_review_info.commodity_name == commodity_name).all()
    for review_info in review_infos:
        review_list.append({'review_url': review_info.review_url,
                            'review_title': review_info.review_title.replace('<em>', '').replace('</em>', ''),
                            'review_img_path': review_info.review_img_path,
                            'review_excerpt': review_info.review_excerpt.replace('<em>', '').replace('</em>', '')})
    return render_template('commodity_contrast.html', commodity_type=commodity_type, commodity_name=commodity_name,
                           info=info, price_list=price_list, review_list=review_list, other_info=other_info)


@first.route('/collection/', methods=['GET', 'POST'])
def collection():
    if 'username' in session:
        user_collect = user_collection()
        user = User()
        if request.method == 'POST':
            now_user_id = user.query.filter(User.username == session['username']).all()[0].user_id
            if request.form.get('collection_flag') == '1':
                user_collect.user_id = now_user_id
                user_collect.commodity_info_id = request.form.get('price_id')
                user_collect.save()
                return '收藏成功'
            else:
                now_collcet = user_collect.query.filter(user_collection.user_id == now_user_id, user_collection.commodity_info_id == request.form.get('price_id')).all()[0]
                user_collect.delete(now_collcet)
                return '取消收藏成功'
        else:
            price_info = commodity_price_info()
            now_user_id = user.query.filter(User.username == session['username']).all()[0].user_id
            collection_id_list = [i.commodity_info_id for i in user_collect.query.filter(user_collection.user_id == now_user_id).all()]
            collection_sum = len(collection_id_list)
            price_infos = price_info.query.filter(commodity_price_info.id.in_(collection_id_list)).all()
            price_list = []
            for i in price_infos:
                price_list.append({'price': i.price,
                                   'price_title': i.price_title,
                                   'price_url': i.price_url,
                                   'price_img_path': i.price_img_path,
                                   'price_id': i.id,
                                   'collection_flag': 1})
            return render_template('my_collction.html', collection_sum=collection_sum, price_list=price_list)
    else:
        return abort(404)


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
