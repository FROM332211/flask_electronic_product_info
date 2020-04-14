import requests
import re


def phone_info_spider():
    content = requests.get('https://product.pconline.com.cn/mobile/miui/').text
    info_name_img_list = re.findall(r'.*<a href="(.*)?" target="_blank">\s+<img class=".*?" width=".*?" height=".*?" alt="(.*?)" title=".*?" src=".*?" #src="(.*)?" /></a>.*', content)
    info_name_img_list = info_name_img_list[:8]
    print(info_name_img_list)
    for i in info_name_img_list:
        url = 'http:'+i[0][0:-5]+'_detail.html'
        print(url)
    return content


# phone_info_spider()

content = requests.get('https://product.pconline.com.cn/mobile/miui/1234200_detail.html').text
print(content)
info_list = re.findall(r'.*', content)
print(info_list)