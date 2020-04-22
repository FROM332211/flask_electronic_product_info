from urllib.parse import quote
import requests
import re
import json
import random
import time
from aip import AipOcr

from APP.model import commodity_price_info, commodity_base_info

APP_ID = '19255460'
API_KEY = '3tYdMSFYCOqp3gOb6Hgnf3Tt'
SECRET_KEY = 'TqzG9uQmfaetbrzp2V7sw4VKVc6fncK2'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def search_taobao(commodity_name, commodity_type, commodity_brand):
    q = quote(commodity_name)
    n = 0
    price_num = 0  # 已入库价格计数器
    while n < 40 and price_num < 10:  # 只爬取第一页的数据并且最多获取10条价格数据
        url = 'https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id' \
              '=staobaoz_20200421&ie=utf8&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s={}'.format(q, str(n))
        headers = {
            'path': '/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200421&ie=utf8'.format(
                q),
            'scheme': 'https',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'cookie': 'thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16f1c1a799b2b9-0064c69be5b999-6701434-144000-16f1c1a799c3eb; cna=kaXGFR5U4W4CATrQwIjT2ad/; _uab_collina=157796023237770396772964; miid=331008241857894789; tracknick=%5Cu7EC8121%5Cu70B9; tg=0; sgcookie=Q6ETBta4pHG11aCE6yJT; _cc_=URm48syIZQ%3D%3D; enc=dvUD7c2SSvLDf3PfpKhT4c0ih7AYibnlQONkTrwVmNZhZBsCV0vROB0rDkw3zGvgkZVzc%2B4yHX3fqvXPRLlAVw%3D%3D; t=7a04dc490fca1d161f04fe3818285e0c; tfstk=cmPdBpsvYGjnabaE37BiNgytpFScZvYKqeiJwaO00bTOhmORiMN0My3Gd4-K6NC..; _m_h5_tk=10d4f76be2b1d8cd3505d90d54f4675e_1587205075856; _m_h5_tk_enc=e4070efe8f32c43848a29bf542ffff2e; mt=ci%3D-1_1; cookie2=1ddccf1c818ce083034589530a51b61f; v=0; _tb_token_=eee3a57b77b3b; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=CA43D6E5096C393743095D4F07D21299; isg=BIuL3Ha9UcxCCo45Wih8c25eGi91IJ-i57UvPv2Jb0ohHKp-hPR38n3-9hzyOvea; l=eBIns7yRqbeLfGvEBO5wqbIKLU7toIOb8rVy20wtPIHca6TCtFgUoNQcLLtDSdtjgtfjGeKPijrhsRnkPZzdg2HvCbKrCyCljY96-'
        }
        res = requests.get(url, headers=headers)
        try:
            res = re.findall(r'g_page_config = ({.*})', res.text)[0]
        except:
            raise print('出错')
        res = json.loads(res)
        try:
            res = res['mods']['itemlist']['data']['auctions']  # 会出现没有商品的情况
        except:
            break
        for i in res:
            n += 1
            group = re.findall(r'{}'.format(commodity_name).replace(' ', ''), i['raw_title'].replace(' ', ''),
                               re.I)  # 对淘宝商品标题进行过滤，标题中存在查询的商品名才进行下一步
            if len(group) > 0:
                price_num += 1
                if price_num > 10:
                    break
                img_url = i['pic_url']
                # orc_res = client.basicGeneralUrl('http:' + img_url)
                # print(orc_res)
                # for word in orc_res['words_result']:
                #     if len(re.findall(r'{}'.format(commodity_name), word['words'])) > 0:
                img_path = '/static/price_info/{}_{}.jpg'.format(commodity_name.replace(' ', ''), n)
                img_file = open('APP' + img_path, 'wb')
                img = requests.get('http:' + img_url)
                # print(img)
                img_file.write(img.content)
                img_file.close()
                Commodity_price_info = commodity_price_info()
                Commodity_price_info.commodity_name = commodity_name
                Commodity_price_info.commodity_type = commodity_type
                Commodity_price_info.commodity_brand = commodity_brand
                Commodity_price_info.price = i['view_price']
                Commodity_price_info.price_url = i['detail_url']
                Commodity_price_info.price_title = i['raw_title']
                Commodity_price_info.price_img_path = img_path
                Commodity_price_info.save()
        time.sleep(random.randint(0, 5))


def taobao_spider():
    Commodity_base_info = commodity_base_info()
    commodity_infos = Commodity_base_info.query.all()
    for commodity in commodity_infos:
        print(commodity.commodity_name)
        search_taobao(commodity.commodity_name, commodity.commodity_type, commodity.commodity_brand)

# phone = ['小米9', '小米10', '小米10Pro']
# for p in phone:
#     print(p)
#     n = 0
#     num = 0
#     while num < 50:
#         print(n)
#         num = search_taobao(n, p, num)
#         n += 44
