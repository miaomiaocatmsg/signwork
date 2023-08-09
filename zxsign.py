'''
new Env('知轩藏书 签到');

'''




import os
import requests
import json


ZX_COOKIES=os.getenv("ZX_COOKIE")


def sign():
    zxurl = "https://zxcstxt.com/wp-admin/admin-ajax.php"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Cookie': ZX_COOKIES,
    'Host': 'zxcstxt.com',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://zxcstxt.com/'
    }
    data = {'action': 'user_checkin'}

    response = requests.post(url=zxurl, headers=headers,data=data)
    result = json.loads(response.text)
    print("签到结果：",result['msg'])
        



if ZX_COOKIES is None:
    print("未获取到 知轩藏书 Cookies 请重新获取")
else:
    print("已获取到 知轩藏书 Cookies 准备开始签到 ")
    sign()








