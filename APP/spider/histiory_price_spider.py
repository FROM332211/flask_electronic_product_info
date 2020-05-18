import copy

import requests
import re
import time
import random
import threading
import queue
from APP.model import commodity_price_info, commodity_history_price


class price_spider(object):
    user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) "
        "AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        # iPhone 6：
        "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 "
        "Mobile/10A5376e Safari/8536.25"]

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.163 Safari/537.36',
               "Proxy-Connection": "keep-alive",
               "Pragma": "no-cache",
               "Cache-Control": "no-cache",
               "DNT": "1",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
               "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                         'application/signed-exchange;v=b3;q=0.9',
               # 'cookie': 'lid=%E7%BB%88121%E7%82%B9; cna=kaXGFR5U4W4CATrQwIjT2ad/; '
               #           'otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; '
               #           'cq=ccp%3D1; hng=CN%7Czh-CN%7CCNY%7C156; '
               #           'enc=dvUD7c2SSvLDf3PfpKhT4c0ih7AYibnlQONkTrwVmNZhZBsCV0vROB0rDkw3zGvgkZVzc'
               #           '%2B4yHX3fqvXPRLlAVw%3D%3D; '
               #           'OZ_1U_2061=vid=vdb8178e32ba17.0&ctime=1587181406&ltime=1587181406; '
               #           'sgcookie=Q6ETBta4pHG11aCE6yJT; t=8e4ae45a7107b2c0a63ee23f5e4c6154; '
               #           'tracknick=%5Cu7EC8121%5Cu70B9; _tb_token_=765e7ebe471d7; '
               #           'cookie2=13e40890f09fa8ce4fa19a244a41cbd4; '
               #           '_m_h5_tk=1ca7e5a22e45f7f2009152522e0ea64f_1589268192852; '
               #           '_m_h5_tk_enc=eac64b834b41112cfcd35efee25d5cf9; sm4=330100; csa=0_0_0_0_0_0_0_0_0_0_0; '
               #           'pnm_cku822=098'
               #           '%23E1hvOpvUvbpvUvCkvvvvvjiPn2cU0jrERsLZQj1VPmPwtjEVPFSW6ji2PsSp1jnviQhvCvvv9U8EvpvVmvvC9j3Euphvmvvv92Dj2VezKphv8vvvvvCvpvvvvvmmM6Cvmh%2BvvvWvphvW9pvvvQCvpvs9vvv2vhCv2RvEvpCWvvY5vvakfw1l%2Bb8rwkM6D7z9d3ODNKClYE7rVB61D7zUaXgqb64B9WmQ%2BulsbSoxfJmKHkx%2Fgjc6kCh7EcqvaNondXIaWXxrzj7JRQhCvvOvCvvvphvPvpvhvv2MMsyCvvpvvvvv; l=eBT3B-QRqHT_ujVbBO5Cnurza779uIdbzsPzaNbMiInGa14FZHR2KNQc715podtjMtfUBeKzEdARfREM7k4LRFZOYKQhKXIpBz99-; isg=BH19BA2l_yYb_1gcdodQndlWjNl3GrFskcKmxj_DLVRidp-oBmlVPMJsIKgwdskk',
               }

    def start(self):
        price_infos = commodity_price_info()
        price_id_list = [[i.id, i.price_url, i.price] for i in price_infos.query.all()]
        # print(price_id_list[0])
        # print('https:' + price_id_list[0][1])
        # print(requests.get('https:' + price_id_list[0][1], headers=self.headers).text)
        # print('https:' + price_id_list[0][1])
        while len(price_id_list) > 0:
            s = []
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+':'+'还剩'+'：' + str(len(price_id_list)))
            for n in range(len(price_id_list)):
                result = self.spider(price_id_list[n][1], price_id_list[n][2])
                # print(result)
                if result in ['未抓取到数据', '获取数据错误']:
                    s.append(price_id_list[n])
                else:
                    self.save(price_id_list[n][0], result)
                # print('------------------------------------------')
                time.sleep(random.randint(0, 5))
            price_id_list = copy.deepcopy(s)
            time.sleep(60)

    def spider(self, url, baseprice):
        self.headers['user-agent'] = self.get_user_agent()
        try:
            result = requests.get('https:' + url, headers=self.headers, timeout=5)  # 获取商品详情页
        except:
            return '获取数据错误'
        price_info = re.findall(r'TShop.Setup\(([\S\s]*?)\);', result.text)  # 提取出价格配置信息
        # print(price_info[0])
        if len(price_info) == 0:
            price_info = re.findall(r'skuMap[ ]*?:[\w\W]*?{([\s\S]*?)\);', result.text)
        if len(price_info) > 0:
            prices = re.findall(r'"price":"(.*?)"', price_info[0])
            price = baseprice
            for i in prices:
                if float(i) < float(price) and abs(float(i) - float(baseprice)) < 500:
                    price = i
            return price
        else:
            return '未抓取到数据'

    def get_proxiex(self, n):
        if n == 0:
            return {}
        else:
            file = open('APP/spider/ip.txt', 'r')
            ip_list = file.readlines()
            # print(ip_list)
            file.close()
            return {'https': ip_list[n - 1][:-1]}

    def save(self, commodity_price_id, price):
        history_price = commodity_history_price()
        history_price.commodity_price_id = commodity_price_id
        history_price.price = price
        history_price.insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        history_price.save()

    def get_user_agent(self):
        return random.choice(self.user_agent)


price_spider = price_spider()
