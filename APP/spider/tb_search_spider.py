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


def search_taobao(commodity_name,commodity_type,commodity_brand):
    q = quote(commodity_name)
    n = 0
    while n < 88:
        url = 'https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id' \
              '=staobaoz_20200418&ie=utf8&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s={}'.format(q, str(n))
        headers = {
            'path': '/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200418&ie=utf8'.format(q),
            'scheme': 'https',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'cookie': 'thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16f1c1a799b2b9-0064c69be5b999-6701434-144000-16f1c1a799c3eb; cna=kaXGFR5U4W4CATrQwIjT2ad/; _uab_collina=157796023237770396772964; miid=331008241857894789; tracknick=%5Cu7EC8121%5Cu70B9; tg=0; sgcookie=Q6ETBta4pHG11aCE6yJT; _cc_=URm48syIZQ%3D%3D; enc=dvUD7c2SSvLDf3PfpKhT4c0ih7AYibnlQONkTrwVmNZhZBsCV0vROB0rDkw3zGvgkZVzc%2B4yHX3fqvXPRLlAVw%3D%3D; t=7a04dc490fca1d161f04fe3818285e0c; v=0; cookie2=1e353733310757126697d6a5b95ea1fe; _tb_token_=f69587e4eee48; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _samesite_flag_=true; tfstk=cmPdBpsvYGjnabaE37BiNgytpFScZvYKqeiJwaO00bTOhmORiMN0My3Gd4-K6NC..; JSESSIONID=88DAC62AA25D509B22A42F29B43ED0AA; isg=BPT0IFT_Fr2RloFUidUbZs37xbJmzRi3pHDgk45X8n8Q-ZZDt96vR7H7eTEhB1AP; l=eBIns7yRqbeLfp3yBO5wZbIKLU79XQAbzsPy20wtPIHca1uhtEBswNQcQjTwSdtjgtfbbeKPijrhsR39Seadg2HvCbKrCyCotYvw-'
        }
        res = requests.get(url, headers=headers)
        try:
            res = re.findall(r'g_page_config = ({.*})', res.text)[0]
        except:
            raise print('出错')
        res = json.loads(res)
        res = res['mods']['itemlist']['data']['auctions']
        for i in res:
            n += 1
            group = re.findall(r'{}'.format(commodity_name).replace(' ', ''), i['raw_title'].replace(' ', ''), re.I)  # 对淘宝商品标题进行过滤，标题中存在查询的商品名才进行下一步
            if len(group) > 0:
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
        search_taobao(commodity.commodity_name,commodity.commodity_type,commodity.commodity_brand)

# phone = ['小米9', '小米10', '小米10Pro']
# for p in phone:
#     print(p)
#     n = 0
#     num = 0
#     while num < 50:
#         print(n)
#         num = search_taobao(n, p, num)
#         n += 44
