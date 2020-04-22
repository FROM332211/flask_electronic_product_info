import requests

# url = 'https://api.bilibili.com/x/web-interface/search/all/v2?context=&page=1&order=&keyword=%E5%B0%8F%E7%B1%B310pro&duration=&tids_1=&tids_2=&__refresh__=true&_extra=&highlight=1&single_column=0&jsonp=jsonp&callback=__jp1'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
#     'Cookie': '''_uuid=7C9D2EC8-29C9-6735-F188-43021A907B1E11162infoc; buvid3=F9BEE31D-7032-4BE4-B761-4572781A39F0155834infoc; sid=cavqtnam; fts=1564456290; _ga=GA1.2.1335949114.1564493047; rpdid=|(m)Y~lmlkR0J'ulYRRmJuuk; CURRENT_FNVAL=16; stardustvideo=1; im_notify_type_10815750=0; LIVE_BUVID=7a98bd029a047736d7c3d2eb875246c3; LIVE_BUVID__ckMd5=43e6050e89c0572f; pgv_pvi=1492658176; _qddaz=QD.1uophv.1pqmbl.k1pzb0ix; LIVE_PLAYER_TYPE=1; laboratory=1-1; CURRENT_QUALITY=116; DedeUserID=10815750; DedeUserID__ckMd5=d56f9e6d9454b1fc; SESSDATA=e1716bd2%2C1601203350%2Cf9c7d*31; bili_jct=09df09425094f70ff3a4f545616bcbf0; bp_t_offset_10815750=377347163677960816; PVID=2''',
#     'Connection': 'keep-alive',
#     'Host': 'api.bilibili.com',
#     'Referer': 'https://search.bilibili.com/all?keyword=%E5%B0%8F%E7%B1%B310'
# }
# print(requests.get(url, headers=headers).text)


url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=QQ&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0'
headers = {
    'authority': 'www.zhihu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'cookie': '_zap=cc5fc7c1-db98-4f0f-9c76-3cc86dbb08aa; d_c0="AEChSBhY0A-PTjIGqbYUCwNCYWN9LK7yuVU=|1564459775"; _xsrf=Tl7fMVZ5TH2Qqi91193UmYFFMMn3fwIe; tshl=; _ga=GA1.2.2128752173.1584335800; __utmv=51854390.100--|2=registration_date=20160909=1^3=entry_date=20160909=1; z_c0=Mi4xblBWdkF3QUFBQUFBUUtGSUdGalFEeGNBQUFCaEFsVk4xVmhnWHdBc1RZUDF0Z1NyMjBXYUJFYU0ycDlTV2VaRHRR|1584597717|581b9d624415b31b860dc3108fb8ee25ac579f2e; tst=h; q_c1=3a2b62dd223349369d4137c54b145a6e|1587007070000|1569045095000; __utma=51854390.2128752173.1584335800.1584449328.1587186417.2; __utmz=51854390.1587186417.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/388417208; _gid=GA1.2.667626534.1587299193; SESSIONID=LgPnBEybnRV7nGL1kBbeiQaGyRNRZTok4q1IqUaz15I; osd=WlsRAUlxT02DW-8hH3v-EYJBngUCNi8b7ROhX3sVFhyyNaJmKYlb1tda4yAZK-xpfC_zeA2IatnVtGjiCdEY788=; JOID=WlAXA0txREuBWe8qGXn8EYlHnAcCPSkZ7xOqWXkXFhe0N6BmIo9Z1NdR5SIbK-dvfi3zcwuKaNnesmrgCdoe7c0=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587359768,1587360140,1587361230,1587362675; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1587368658; KLBRSID=ca494ee5d16b14b649673c122ff27291|1587369034|1587347150',
    'path': '/api/v4/search_v3?t=general&q=QQ&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0',
    'authority': 'www.zhihu.com',
    'referer': 'https://www.zhihu.com/search?type=content&q=QQ',
    'x-api-version': '3.0.91',
    'x-app-za': 'OS=Web',
    'x-requested-with': 'fetch',
    'x-zse-83': '3_2.0',
    'x-zse-86': '1.0_aLx0kT98k0xp6LtyY_xBo0U0r_YfQMFBY_OySTr0UG2Y'
}
res = requests.get(url, headers=headers).text
print(res)