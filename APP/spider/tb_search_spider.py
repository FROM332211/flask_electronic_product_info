from urllib.parse import quote
import requests
import re
import json
import random
import time
from aip import AipOcr

APP_ID = '19255460'
API_KEY = '3tYdMSFYCOqp3gOb6Hgnf3Tt'
SECRET_KEY = 'TqzG9uQmfaetbrzp2V7sw4VKVc6fncK2'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def search_taobao(cookie, n, p, num):
    q = quote(p)
    url = 'https://s.taobao.com/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200403&ie=utf8&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s='.format(q)+str(n)
    headers = {
        'path': '/search?q={}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200404&ie=utf8'.format(q),
        'scheme': 'https',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'cookie': cookie
    }
    res = requests.get(url, headers=headers)
    try:
        res = re.findall(r'g_page_config = ({.*})', res.text)[0]
    except:
        raise print('出错')
    res = json.loads(res)
    res = res['mods']['itemlist']['data']['auctions']
    file = open('test.txt', 'a', encoding='utf8')
    for i in res:
        group = re.findall(r'{}'.format(p), i['raw_title'])
        if len(group) > 0:
            img_url = i['pic_url']
            orc_res = client.basicGeneralUrl('http:'+img_url)
            print(orc_res)
            for word in orc_res['words_result']:
                if len(re.findall(r'{}'.format(p), word['words'])) > 0:
                    num += 1
                    img_name = '{}'.format(p+'-'+str(num))
                    img_file = open(r'D:\pycharm_work\Graduation_data_spider\img\{}_img.jpg'.format(p+'-'+str(num)), 'a+b')
                    img = requests.get('http:'+img_url)
                    print(img)
                    img_file.write(img.content)
                    img_file.close()

                    file.write(p + ',' + i['detail_url'] + ',' + i['raw_title'] + ',' + i['view_price']+','+img_name)
                    file.write('\n')
    file.close()
    time.sleep(random.randint(0, 5))
    return num


if __name__ == '__main__':
    phone = ['小米9', '小米10', '小米10Pro']
    cookie = 'thw=cn; cna=GA3gFis0XlYCAWX0YpTYRd+d; sgcookie=D7wznHwfkcuSQT%2BLmnhF3; tracknick=%5Cu7EC8121%5Cu70B9; _cc_=W5iHLLyFfA%3D%3D; tg=0; enc=gugtnsDHGwBkuzgwWrr7EcvfZmDB9vuO3MG7yhf%2BSgabQjB%2BAziSzeo2N64qS1Odwvm%2B%2BUXWs8FTuCkqij9Etw%3D%3D; tfstk=cX7GB0iVRG-_e8IqaVT1GyhEH64RZDu2EZ7C8Nq7xEyVEtQFi4nE4kb3tdXGkm1..; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci=-1_0; t=1a53b7bb269d0a9e288c9d6b351a6f27; v=0; cookie2=1d97cc9aecd7cd48bb2e95d0ab496650; _tb_token_=3f63950dffb54; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=88538EE4F859C7FFA4073961186F1388; l=dBr5ufnIQhsMeF5hBOfNROlzn3_OuBAb8sPzSfpbEICP_Xfhdg3FWZfOv-TMCnGNnsdDJ3oGfmN0Bo8lyyCqJxpsw3k_J_xZvdTh.; isg=BLW1YtnyB_yHSmORbobyVl2FxDFvMmlEZWRDqDfcYCzNDtQA_odkFJHMWNo4ToH8'
    for p in phone:
        print(p)
        n = 0
        num = 0
        while num < 50:
            print(n)
            num = search_taobao(cookie, n, p, num)
            n += 44
