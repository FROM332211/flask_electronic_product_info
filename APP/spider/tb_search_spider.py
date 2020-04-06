import requests
import re
import json
import random
import time
from urllib.request import quote


def search_taobao(cookie, n, p):
    url_n = url + str(n)
    headers = {
        'path': '/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200403&ie=utf8'.format(q),
        'scheme': 'https',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'cookie': cookie
    }
    res = requests.get(url, headers=headers)
    try:
        res = re.findall(r'g_page_config = ({.*})', res.text)[0]
    except:
        raise Exception('出错')
    res = json.loads(res)
    res = res['mods']['itemlist']['data']['auctions']
    file = open('test.txt', 'a', encoding='utf8')
    no = n
    for i in res:
        group = re.findall(r'{}'.format(p), i['raw_title'])
        if group is not None:
            img_url = i['pic_url']
            img = open(r'F:\spider-img\{}.jpg'.format(p))
            file.write(p + ',' + i['detail_url'] + ',' + i['raw_title'] + ',' + i['view_price'])
            file.write('\n')
    file.close()
    time.sleep(random.randint(0, 5))


if __name__ == '__main__':
    phone = ['小米9', '小米10', '小米10pro']
    cookie = 'thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16f1c1a799b2b9-0064c69be5b999-6701434-144000-16f1c1a799c3eb; cna=kaXGFR5U4W4CATrQwIjT2ad/; _uab_collina=157796023237770396772964; miid=331008241857894789; tracknick=%5Cu7EC8121%5Cu70B9; tg=0; sgcookie=Q6ETBta4pHG11aCE6yJT; _cc_=URm48syIZQ%3D%3D; enc=dvUD7c2SSvLDf3PfpKhT4c0ih7AYibnlQONkTrwVmNZhZBsCV0vROB0rDkw3zGvgkZVzc%2B4yHX3fqvXPRLlAVw%3D%3D; t=b9e969592ae444e8840c3ec0ae39b5e3; v=0; cookie2=16c8bd0b5db216646c40c02bb363beb5; _tb_token_=f8313be33763e; JSESSIONID=8CC19384F5119774DCBAD7905FFA16CB; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; isg=BFNThduGCfx1IcaRQjC0q-am4td9COfK9x4lzgVwRnKphHAmjNwEGuKWvvzqJD_C; l=dBIns7yRqbeLfkz9BOfgmbIKLU795IRf1sPy20wtPICPO51e5jIfWZfz0oLwCnGNnsIDJ3oGfmN0BXL5PyCqJxpsw3k_J_YZ3d8h.'
    for p in phone:
        print(p)
        q = quote(p)
        print(q)
        url = 'https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200403&ie=utf8&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s='.format(q)
        n = 0
        while n < 480:
            print(n)
            try:
                search_taobao(cookie, n, p)
            except:
                get_cookie()
            n += 48
