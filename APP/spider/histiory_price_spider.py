import requests
import re
import time
from APP.model import commodity_price_info


class price_spider(object):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.163 Safari/537.36',
               'cookie': 'thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; '
                         'hng=CN%7Czh-CN%7CCNY%7C156; '
                         'UM_distinctid=16f1c1a799b2b9-0064c69be5b999-6701434-144000-16f1c1a799c3eb; '
                         'cna=kaXGFR5U4W4CATrQwIjT2ad/; miid=331008241857894789; tracknick=%5Cu7EC8121%5Cu70B9; tg=0; '
                         'sgcookie=Q6ETBta4pHG11aCE6yJT; _cc_=URm48syIZQ%3D%3D; '
                         'enc=dvUD7c2SSvLDf3PfpKhT4c0ih7AYibnlQONkTrwVmNZhZBsCV0vROB0rDkw3zGvgkZVzc'
                         '%2B4yHX3fqvXPRLlAVw%3D%3D; '
                         'tfstk=cdn1B9iJj1fsIAmNYj9U7wB-KirfZSRQKFNtC2H1ck6OCvM1iAjzN5Xro6jLyJ1..; '
                         '_samesite_flag_=true; cookie2=118b5135ee12ad9741e8d1d50277ea0d; '
                         't=3cece808f1d923f668f7bf0c706175b9; _tb_token_=5ab573bb3f1e4; v=0; '
                         '_m_h5_tk=fa953b87cf00f18fbb8046827d333c43_1589018150582; '
                         '_m_h5_tk_enc=3b1bc54cfa8967c51a8d520e82cc53f8; mt=ci%3D-1_1; '
                         'isg=BMvLFe4xESQWnU3gfgdybnHkWm-1YN_ic_gQED3IiophXOu-xTRbMmv9Mlyy_Dfa; '
                         'l=eB_hXUQHQ6G8pevOBOfwnurza77OOIRAguPzaNbMiT5P_k5y5jK1WZbyfaL2CnGVh6Y9R3ykIQI6BeYBqQd'
                         '-nxvte5DDw3kmn'}

    def start(self):
        price_infos = commodity_price_info()
        price_id_list = [[i.id, i.price_url, i.price] for i in price_infos.query.all()]
        # print(price_id_list[0])
        # print('https:' + price_id_list[0][1])
        # print(requests.get('https:' + price_id_list[0][1], headers=self.headers).text)
        # print('https:' + price_id_list[0][1])
        for price_id in price_id_list:
            self.spider(price_id[1], price_id[2])

    def spider(self, url, baseprice):
        result = requests.get('https:' + url, headers=self.headers)  # 获取商品详情页
        price_info = re.findall(r'TShop.Setup\(([\S\s]*?)\);', result.text)  # 提取出价格配置信息
        print(price_info[0])
        prices = re.findall(r'"price":"(.*?)"', price_info[0])
        price = 0
        for i in price:

            print(prices)
        time.sleep(5)
        return price


price_spider = price_spider()
