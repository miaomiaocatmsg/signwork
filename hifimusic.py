'''
cron: 0 0 0,5 * * *
new Env('hifini音乐网 签到');

'''




import os
import requests
import json
from json import JSONDecodeError



HIFI_COOKIE=os.getenv("HIFI_COOKIE")
HIFI_COOKIE="bbs_sid=hkkgt8r5i1hjn56mbjl481jh45; bbs_token=ReaaTtZWPkUCUbqLmrVSmGtmahLAMajwrVXmugDeuzyjl9irodc6TVoqaZ_2F8JTvWJVj1ZcKSyB4BJ5AKp0jMJ2FSQkxHe1FR"

def sign():
    hifiurl = "https://hifini.com/sg_sign.htm"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Cookie': HIFI_COOKIE,
    'Host': 'hifini.com',
    'Connection': 'keep-alive',
    'Accept': 'text/plain, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://hifini.com/sg_sign.htm'
    }


    response = requests.post(url=hifiurl, headers=headers)
    try:
        result = json.loads(response.text)
        print("签到结果：",result['message'])
    except JSONDecodeError:
        result = response.text
        print("出现预期外的错误",result)
        

        



if HIFI_COOKIE is None:
    print("未获取到 hifini音乐网 Cookies 请重新获取")
else:
    print("已获取到 hifini音乐网 Cookies 准备开始签到 ")
    sign()








