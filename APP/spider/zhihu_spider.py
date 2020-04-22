import json
import random
import time
from urllib.parse import quote

import pyautogui
import win32clipboard
import pyperclip
import requests

from APP.model import commodity_base_info, commodity_review_info

pyautogui.FAILSAFE = True


def get_x_zse_86(commodity_name):
    time.sleep(3)
    x, y, width, height = pyautogui.locateOnScreen('APP/spider/chrom.png')
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click(x, y)
    pyautogui.hotkey('f5')
    time.sleep(3)
    x, y, width, height = pyautogui.locateOnScreen('APP/spider/zhihu_1.png')
    pyautogui.click(x - 100, y, duration=0.5)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)
    pyperclip.copy(commodity_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    # pyautogui.click(x, y, duration=0.5)
    time.sleep(2)
    pyautogui.click(253, 988, duration=0.5)
    pyautogui.moveTo(853, 988, duration=0.5)
    pyautogui.scroll(-10000)
    time.sleep(2)
    x, y, width, height = pyautogui.locateOnScreen('APP/spider/zhihu_2.png')
    pyautogui.click(x + 150, y, clicks=2)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c')
    x, y, width, height = pyautogui.locateOnScreen('APP/spider/pycharm.png')
    pyautogui.click(x, y)

    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
    win32clipboard.CloseClipboard()
    return str(text)


def zhihu_search_spider(commodity_type, commodity_brand, commodity_name, text):
    print(text)
    text = text[2:-1]
    print(text)
    # print(quote(commodity_name))
    url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0'.format(
        quote(commodity_name))
    headers = {
        'authority': 'www.zhihu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'cookie': '_zap=cc5fc7c1-db98-4f0f-9c76-3cc86dbb08aa; d_c0="AEChSBhY0A-PTjIGqbYUCwNCYWN9LK7yuVU=|1564459775"; _xsrf=Tl7fMVZ5TH2Qqi91193UmYFFMMn3fwIe; tshl=; _ga=GA1.2.2128752173.1584335800; __utmv=51854390.100--|2=registration_date=20160909=1^3=entry_date=20160909=1; z_c0=Mi4xblBWdkF3QUFBQUFBUUtGSUdGalFEeGNBQUFCaEFsVk4xVmhnWHdBc1RZUDF0Z1NyMjBXYUJFYU0ycDlTV2VaRHRR|1584597717|581b9d624415b31b860dc3108fb8ee25ac579f2e; tst=h; q_c1=3a2b62dd223349369d4137c54b145a6e|1587007070000|1569045095000; __utma=51854390.2128752173.1584335800.1584449328.1587186417.2; __utmz=51854390.1587186417.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/388417208; _gid=GA1.2.667626534.1587299193; SESSIONID=LgPnBEybnRV7nGL1kBbeiQaGyRNRZTok4q1IqUaz15I; osd=WlsRAUlxT02DW-8hH3v-EYJBngUCNi8b7ROhX3sVFhyyNaJmKYlb1tda4yAZK-xpfC_zeA2IatnVtGjiCdEY788=; JOID=WlAXA0txREuBWe8qGXn8EYlHnAcCPSkZ7xOqWXkXFhe0N6BmIo9Z1NdR5SIbK-dvfi3zcwuKaNnesmrgCdoe7c0=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587359768,1587360140,1587361230,1587362675; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1587368462; _gat_gtag_UA_149949619_1=1; KLBRSID=ca494ee5d16b14b649673c122ff27291|1587368469|1587347150',
        'path': '/api/v4/search_v3?t=general&q={}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0'.format(
            quote(commodity_name)),
        'authority': 'www.zhihu.com',
        'referer': 'https://www.zhihu.com/search?type=content&q={}'.format(quote(commodity_name)),
        'x-api-version': '3.0.91',
        'x-app-za': 'OS=Web',
        'x-requested-with': 'fetch',
        'x-zse-83': '3_2.0',
        'x-zse-86': text
    }
    res = requests.get(url, headers=headers).text
    # print(res)
    # print('================')
    try:
        res = json.loads(res)['data']
    except:
        raise Exception('请更换x-zse-86')
    # print(res)
    n = 0
    for review in res:
        if review['type'] in ['one_box', 'search_result'] and review['object']['type'] == 'answer':
            if 'content_list' in review['object']:
                for content in review['object']['content_list']:
                    title = content['question']['name']
                    # print(title)
                    url = 'https://www.zhihu.com/answer/' + content['id']
                    # print(url)
                    excerpt = content['excerpt']
                    # print(excerpt)
                    review_dict = {'url': url, 'title': title, 'excerpt': excerpt}
                    Commodity_review_info = commodity_review_info()
                    Commodity_review_info.commodity_name = commodity_name
                    Commodity_review_info.commodity_type = commodity_type
                    Commodity_review_info.commodity_brand = commodity_brand
                    Commodity_review_info.review_title = review_dict['title']
                    Commodity_review_info.review_excerpt = review_dict['excerpt']
                    Commodity_review_info.review_url = review_dict['url']
                    Commodity_review_info.save()
                    n += 1
            else:
                # print(review)
                title = review['object']['question']['name']
                # print(title)
                url = 'https://www.zhihu.com/answer/' + review['object']['id']
                # print(url)
                excerpt = review['object']['excerpt']
                # print(excerpt)
                review_dict = {'url': url, 'title': title, 'excerpt': excerpt}
                n += 1
                Commodity_review_info = commodity_review_info()
                Commodity_review_info.commodity_name = commodity_name
                Commodity_review_info.commodity_type = commodity_type
                Commodity_review_info.commodity_brand = commodity_brand
                Commodity_review_info.review_title = review_dict['title']
                Commodity_review_info.review_excerpt = review_dict['excerpt']
                Commodity_review_info.review_url = review_dict['url']
                # Commodity_review_info.zhihu_x_zse_86 = text
                Commodity_review_info.save()
        if n > 10:
            break
    time.sleep(random.randint(1, 5))


def zhihu_review_spider():
    Commodity_base_info = commodity_base_info()
    Commodity_infos = Commodity_base_info.query.all()
    file = open('APP/spider/zhihu_{}.txt'.format(time.strftime('%m%d')), 'x')
    for commodity in Commodity_infos:
        print(commodity.commodity_name)
        text = get_x_zse_86(commodity.commodity_name)
        # print(text)
        file.write(commodity.commodity_name+','+text[2:]+'/n')
        zhihu_search_spider(commodity.commodity_type, commodity.commodity_brand, commodity.commodity_name, text)
    file.close()
