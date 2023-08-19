'''
cron: 0 0 0,5 * * *
new Env('PicoXR网 签到');

'''

import os
import requests
import json


PICOXR_COOKIE=os.getenv("PICOXR_COOKIE")


def sign():
    url = "https://bbs.picoxr.com/ttarch/api/growth/v1/checkin/create?app_id=264482&service_id=0&lang=zh-Hans-CN"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Host':'bbs.picoxr.com',
    'Connection':'keep-alive',
    'Content-Type':'application/json',
    'Accept':'application/json, text/plain, */*',
    'Referer':'https://bbs.picoxr.com/user-growth/checkin',
    'Cookie': PICOXR_COOKIE,
    }


    response = requests.post(url=url, headers=headers,)
    result = json.loads(response.text)
    pcsign=result['data']['info']["sum_count"]
    jf=result['data']['point_records'][0]['score']
    if pcsign==0:
        print("今日已签到过 签到积分：",jf)
    else:
        print("本次签到成功 签到积分：",jf)

def dailyVisit():
    url="https://bbs.picoxr.com/ttarch/api/growth/v1/user/online?app_id=264482&service_id=0&lang=zh-Hans-CN"
    headers={
        'Host':'bbs.picoxr.com',
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/115.0.0.0Safari/537.36',
        'Content-Type':'application/json',
        'Accept':'application/json,text/plain,*/*',
        'Origin':'https://bbs.picoxr.com',
        'Referer':'https://bbs.picoxr.com/?is_new_connect=0&is_new_user=0',
        'Cookie': PICOXR_COOKIE,

    }

    response = requests.post(url=url, headers=headers,)
    result = json.loads(response.text)
    print("每日访问任务：",result["data"])




if PICOXR_COOKIE is None:
    print("未获取到 PicoXR网 Cookies 请重新获取")
else:
    print("已获取到 PicoXR网 Cookies 准备开始签到 ")
    dailyVisit()
    sign()















