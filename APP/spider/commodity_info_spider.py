import requests
import re
from bs4 import BeautifulSoup, NavigableString


def get_info(tag):
    return isinstance(tag.next_element, NavigableString)  # and tag.th.string in ['CPU', '运行内存']


def phone_info_spider(bas_url):
    content = requests.get(bas_url).text
    soup = BeautifulSoup(content, 'lxml')
    ul = soup.find_all('ul', {'id': 'J_PicMode'})[0]  # 提取出商品信息列表
    n = 0
    info_list = []
    for li in ul.children:
        info_dict = {}
        if hasattr(li, 'data-follow-id') and n < 6:  # 过滤空的li，只取6个商品
            # print(li)
            # print('========')
            info_url = 'http://detail.zol.com.cn/' + li.a['href']  # 获取商品参数页面URL
            name = re.sub(r'（.*）', '', li.img['alt'])
            for i in info_list:
                if i['name'] == name:
                    break; continue
            img_path = li.img['.src']
            price = li.find_all('b', {'class': 'price-type'})[0].string
            if price == '概念产品':
                continue
            # print(url)
            # print(name)
            # print(img_path)
            info_dict['name'] = name
            info_dict['price'] = price
            info_dict['img_path'] = img_path

            info = requests.get(info_url).text
            info_soup = BeautifulSoup(info, 'lxml')
            info_more_url = 'http://detail.zol.com.cn/' + info_soup.find_all('a', {'class': 'section-more'})[0][
                'href']  # 获取详细参数页面URL
            # print(info_more_url)

            info_more = requests.get(info_more_url).content
            info_more_soup = BeautifulSoup(info_more, 'lxml')
            tables = info_more_soup.find_all('div', {'class': 'detailed-parameters'})[0]  # 找到商品详细信息的div
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
                            if hasattr(tr.th, 'a') and tr.th.a is not None:
                                info_dict[tr.th.a.string] = [i for i in tr.td.span.strings]
                            info_dict[tr.th.string] = [i for i in tr.td.span.strings]
            print(info_dict)
            n += 1
            info_list.append(info_dict)




base_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_613_list_1.html','http://detail.zol.com.cn/cell_phone_index/subcate57_1795_list_1.html','http://detail.zol.com.cn/cell_phone_index/subcate57_1673_list_1.html','http://detail.zol.com.cn/cell_phone_index/subcate57_544_list_1.html','http://detail.zol.com.cn/cell_phone_index/subcate57_98_list_1.html','http://detail.zol.com.cn/cell_phone_index/subcate57_34645_list_1.html']
for base_url in base_urls:
    phone_info_spider(base_url)
