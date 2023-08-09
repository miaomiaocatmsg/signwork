'''
cron: 0 0 1 * * *
new Env('TLY 签到');
Author: Mic_c
'''



import time
import requests
import base64
import json
import os
from datetime import datetime, timedelta

cookie =os.getenv("TLY_COOKIE")
token = os.getenv("TLY_TOKEN")



# token 在 http://www.bhshare.cn/imgcode/gettoken/ 自行申请

def get_img_code_by_url(imgurl):
    data = {
        'token': token,
        'type': 'online',
        'uri': imgurl
    }
    response = requests.post('http://www.bhshare.cn/imgcode/', data=data)
    result = json.loads(response.text)
    if result['code'] == 200:
        return result['data']
    else:
        return 'error'


def get_string_between(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def sign():
    sign_url = "https://tly31.com/modules/index.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
               'Cookie': cookie}

    res = requests.get(url=sign_url, headers=headers).text
    sign_time = get_string_between(res, '<p>上次签到时间：<code>', '</code></p>')
    last_sign_time = datetime.strptime(sign_time, "%Y-%m-%d %H:%M:%S")
    elapsed_time = datetime.now() - last_sign_time
    print("上次签到时间",sign_time)

    if elapsed_time > timedelta(hours=24):
        print("距上次签到时间大于 24 小时，可签到")

        is_signed = False
        while not is_signed:
            # 获取验证码图片
            captcha_url = "https://tly31.com/other/captcha.php"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                       'Cookie': cookie}
            img_content = requests.get(url=captcha_url, headers=headers).content
            base64_data = base64.b64encode(img_content)
            captcha_code = get_img_code_by_url('data:image/jpeg;base64,' + str(base64_data, 'utf-8'))

            sign_url_with_captcha = "https://tly31.com/modules/_checkin.php?captcha=" + captcha_code.upper()
            res = requests.get(url=sign_url_with_captcha, headers=headers).text
            print(res)

            if "流量" in res:
                is_signed = True
            else:
                print("未签到成功，沉睡 3 秒再来一次")
                time.sleep(3)
    else:
        print("还未到时间！")

if cookie is None:
    print("未获取到 TLY Cookies 请重新获取")
else:
    print("已获取到 TLY Cookies 准备开始签到 ")
    if token is None:
        print("未获取到 TLY token 请自行申请token")
    else:
        print("已获取到 TLY token 准备开始签到 ")
        sign()



