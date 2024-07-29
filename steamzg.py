'''
cron: 0 0 0,5 * * *
new Env('小叽资源 签到');
Author: 福吧 Mic_c
'''
import os
import requests
import json
from notify import send  # 导入青龙消息通知模块

STEAMZG_URL = "https://steamzg.com/wp-admin/admin-ajax.php"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

def steam_zg_get_fstnonce():
    url = (f"{STEAMZG_URL}?action=5aa951b59f2bef7cf077be0dc6a8a328&0a5a048083df96f3eaeeb9da7bcfc86f%5Btype%5D=checkUnread&71ad17b10b3a0670bf4ba42ceb5e4178%5Btype%5D=getHomepagePosts")
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "steamzg.com",
        "Origin": "https://steamzg.com",
        "User-Agent": USER_AGENT,
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    nonce = data["_nonce"]
    return nonce


def steam_zg_login(nonce,username, password):
    url = f"{STEAMZG_URL}?_nonce={nonce}&action=ad4f94c6b5a3bc58881ce06f757265f4&type=login"
    files = {
        'email': (None, username),
        'pwd': (None, password),
        'type': (None, 'login')
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "steamzg.com",
        "Origin": "https://steamzg.com",
        "User-Agent": USER_AGENT,
    }
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.headers.get("Set-Cookie")
    else:
        response.raise_for_status()

def steam_zg_lottery(cookies, nonce, lottery_id):
    url = f"{STEAMZG_URL}?_nonce={nonce}&action=0d7dddc812e0549a899a423092756535&type=raffle"
    files = {'itemId': (None, lottery_id)}
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "steamzg.com",
        "Origin": "https://steamzg.com",
        "User-Agent": USER_AGENT,
        "Cookie": cookies,
    }
    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json().get("msg")

def steam_zg_sign(cookies, nonce):
    url = f"{STEAMZG_URL}?_nonce={nonce}&action=f3b721e08e5694f00d57c082de42af46&type=goSign"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "steamzg.com",
        "User-Agent": USER_AGENT,
        "Cookie": cookies,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("msg")

def steam_zg_get_nonce(cookies):
    url = (f"{STEAMZG_URL}?action=5aa951b59f2bef7cf077be0dc6a8a328"
           "&f3b721e08e5694f00d57c082de42af46%5Btype%5D=checkSigned"
           "&0a5a048083df96f3eaeeb9da7bcfc86f%5Btype%5D=checkUnread"
           "&a6ba16f28836396ec77803042d6b2506%5Btype%5D=getFollowBtnStatus"
           "&a6ba16f28836396ec77803042d6b2506%5BfollowerId%5D=1"
           "&0d7dddc812e0549a899a423092756535%5Btype%5D=getItems"
           "&08f9e5e770ccc32000f1762e3f115e5d%5Btype%5D=getUnreadCount"
           "&ba5a28e1991775cf69d434de40721eb7%5Btype%5D=getAuthorProfile"
           "&ba5a28e1991775cf69d434de40721eb7%5BauthorId%5D=1")
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "steamzg.com",
        "Origin": "https://steamzg.com",
        "User-Agent": USER_AGENT,
        "Cookie": cookies,
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    nonce = data["_nonce"]
    baisong_id = data["customAccountPointLottery"]["items"][1]["id"]
    baipiao_id = data["customAccountPointLottery"]["items"][2]["id"]
    msg1=steam_zg_sign(cookies, nonce)
    msg2=steam_zg_lottery(cookies, nonce, baisong_id)
    msg3=steam_zg_lottery(cookies, nonce, baisong_id)
    msg4=steam_zg_lottery(cookies, nonce, baipiao_id)
    msg5=steam_zg_lottery(cookies, nonce, baipiao_id)

    send("小叽资源",msg1 + "\n" + msg2 + "\n" + msg3 + "\n" + msg4 + "\n" + msg5)

if __name__ == "__main__":
    account = os.getenv("STEAMZG_ACCOUNT")
    username, password = account.split('#')
    nonce=steam_zg_get_fstnonce()
    cookies = steam_zg_login(nonce,username, password)
    steam_zg_get_nonce(cookies)
