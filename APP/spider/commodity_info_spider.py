import re
import requests
from bs4 import BeautifulSoup

from APP.ext import db
from APP.model import commodity_base_info


def phone_info_spider(bas_url):
    content = requests.get(bas_url).text
    soup = BeautifulSoup(content, 'lxml')
    ul = soup.find_all('ul', {'id': 'J_PicMode'})[0]  # 提取出商品信息列表
    commodity_type = [i for i in soup.find_all('div', {'class': 'breadcrumb'})[0].strings][2]  # 找到商品的种类
    commodity_brand = [i for i in soup.find_all('div', {'id': 'J_FilterSelected'})[0].strings][1]  # 找到商品的名称
    n = 0
    info_list = []
    for li in ul.children:
        info_dict = {}
        if hasattr(li, 'data-follow-id') and n < 6:  # 过滤空的li，只取6个商品
            # print(li)
            # print('========')
            info_url = 'http://detail.zol.com.cn/' + li.a['href']  # 获取商品参数页面URL
            name = re.sub(r'（.*）', '', li.img['alt'])
            name = re.sub(r'\(.*\)', '', name)
            flag = 0
            for i in info_list:
                if i['commodity_name'] == name:
                    flag = 1
                    break
            if flag == 1:
                continue
            img_url = li.img['.src']
            img_path = '/static/base_info/{}.jpg'.format(name.replace(' ', ''))
            img = requests.get(img_url).content
            img_file = open('APP'+img_path, 'wb')
            img_file.write(img)
            img_file.close()
            price = li.find_all('b', {'class': 'price-type'})[0].string
            if price == '概念产品':
                continue
            # print(url)
            # print(name)
            # print(img_path)
            info_dict['commodity_name'] = name
            info_dict['commodity_base_price'] = price
            info_dict['img_path'] = img_path

            info = requests.get(info_url).text
            info_soup = BeautifulSoup(info, 'lxml')
            info_more_url = 'http://detail.zol.com.cn/' + info_soup.find_all('a', {'class': 'section-more'})[0][
                'href']  # 获取详细参数页面URL
            # print(info_more_url)

            info_more = requests.get(info_more_url).content
            info_more_soup = BeautifulSoup(info_more, 'lxml')
            tables = info_more_soup.find_all('div', {'class': 'detailed-parameters'})[0]  # 找到商品详细信息的div
            info_text = ''
            for table in tables.children:
                if table.name == 'table':  # 过滤掉除了table的标签
                    # print(table)
                    for tr in table.children:  # 取出table中的所有列名和值
                        # print(tr)
                        if hasattr(tr, 'th') and tr.th is not None:
                            # print(tr)
                            # print(tr.th)
                            # print(tr.td)
                            # print('------------')
                            # print(tr.td.span.contents)
                            # print('===================')
                            if hasattr(tr.th, 'a') and tr.th.a is not None:  # 取出所有值并拼成一条str
                                th_name = tr.th.a.string
                            #     info_dict[tr.th.a.string] = [i for i in tr.td.span.strings]
                            # info_dict[tr.th.string] = [i for i in tr.td.span.strings]
                            else:
                                th_name = tr.th.string
                            if th_name is None:
                                continue
                            tr_string = ''
                            for string in tr.td.span.stripped_strings:
                                tr_string += string
                                tr_string += ','
                            info_text += th_name + ':' + tr_string
                            info_text += ';'
            info_dict['info'] = info_text
            # print(info_dict)
            n += 1
            info_list.append(info_dict)

    for info in info_list:
        info['commodity_type'] = commodity_type
        info['commodity_brand'] = commodity_brand
    return info_list


def base_infoz():
    base_infos = []
    base_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_613_list_1.html',  # 手机
                 'http://detail.zol.com.cn/cell_phone_index/subcate57_1795_list_1.html',
                 'http://detail.zol.com.cn/cell_phone_index/subcate57_1673_list_1.html',
                 'http://detail.zol.com.cn/cell_phone_index/subcate57_544_list_1.html',
                 'http://detail.zol.com.cn/cell_phone_index/subcate57_98_list_1.html',
                 'http://detail.zol.com.cn/cell_phone_index/subcate57_34645_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_160_list_1.html',  # 笔记本
                 'http://detail.zol.com.cn/notebook_index/subcate16_21_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_544_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_223_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_227_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_613_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_1191_list_1.html',
                 'http://detail.zol.com.cn/notebook_index/subcate16_34645_list_1.html',
                 'http://detail.zol.com.cn/cpu/amd/',  # CPU
                 'http://detail.zol.com.cn/cpu/intel/',
                 'http://detail.zol.com.cn/motherboard/gigabyte/',  # 主板
                 'http://detail.zol.com.cn/motherboard/asus/',
                 'http://detail.zol.com.cn/vga/colorful/',  # 显卡
                 'http://detail.zol.com.cn/vga/galaxy/',
                 'http://detail.zol.com.cn/memory/corsair/',  # 内存
                 'http://detail.zol.com.cn/memory/gskill/',
                 'http://detail.zol.com.cn/solid_state_drive/samsung/',  # 固态
                 'http://detail.zol.com.cn/solid_state_drive/toshiba/',
                 'http://detail.zol.com.cn/power/corsair/',  # 电源
                 'http://detail.zol.com.cn/power/coolermaster/']
    for base_url in base_urls:
        info_list = phone_info_spider(base_url)
        for base_info in info_list:
            Commodity_info = commodity_base_info()
            Commodity_info.commodity_brand = base_info['commodity_brand']
            Commodity_info.commodity_name = base_info['commodity_name']
            Commodity_info.commodity_type = base_info['commodity_type']
            Commodity_info.img_path = base_info['img_path']
            Commodity_info.info = base_info['info']
            Commodity_info.commodity_base_price = base_info['commodity_base_price']
            Commodity_info.save()
            print(base_info)
            base_infos.append(base_info)
