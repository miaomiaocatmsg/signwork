'''
cron: 0 0 0 * * *
new Env('steamZg 签到');

'''


import requests
import json



def SteamZgLogin(username,password):

    url = "https://steamzg.com/wp-admin/admin-ajax.php?_nonce=8ba8c0b6e2&action=ad4f94c6b5a3bc58881ce06f757265f4&type=login"

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }

    response = requests.post(url, files=files, headers=headers)
    return(response.headers.get("Set-Cookie"))

def SteamZgLottery(Cookies,nonce,lotteryId):
        
        url = "https://steamzg.com/wp-admin/admin-ajax.php?_nonce="+nonce+"&action=0d7dddc812e0549a899a423092756535&type=raffle"
        print(url)
        files = {
            'itemId': (None, lotteryId)
        }
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "steamzg.com",
            "Origin": "https://steamzg.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Cookie":Cookies,
    }
        response = requests.post(url, files=files, headers=headers)
        S1 = json.loads(response.text)
        msg=S1["msg"]
        return(msg)

def SteamZgSign(Cookies,nonce):

    url = "https://steamzg.com/wp-admin/admin-ajax.php?_nonce="+nonce+"&action=f3b721e08e5694f00d57c082de42af46&type=goSign"
    payload = ""
    headers = {
        'Accept': "*/*",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Connection': "keep-alive",
        'Host': "steamzg.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        'Cookie': Cookies,

    }
    response = requests.request("GET", url, data=payload, headers=headers)

    S1 = json.loads(response.text)
    msg=S1["msg"]
    return(msg)

def SteamZgGetNonce(Cookies):

    url = "https://steamzg.com/wp-admin/admin-ajax.php?action=5aa951b59f2bef7cf077be0dc6a8a328&f3b721e08e5694f00d57c082de42af46%5Btype%5D=checkSigned&0a5a048083df96f3eaeeb9da7bcfc86f%5Btype%5D=checkUnread&a6ba16f28836396ec77803042d6b2506%5Btype%5D=getFollowBtnStatus&a6ba16f28836396ec77803042d6b2506%5BfollowerId%5D=1&0d7dddc812e0549a899a423092756535%5Btype%5D=getItems&08f9e5e770ccc32000f1762e3f115e5d%5Btype%5D=getUnreadCount&ba5a28e1991775cf69d434de40721eb7%5Btype%5D=getAuthorProfile&ba5a28e1991775cf69d434de40721eb7%5BauthorId%5D=1"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "steamzg.com",
        "Origin": "https://steamzg.com",
        "Cookie":Cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }

    response = requests.post(url, headers=headers)
    S1 = json.loads(response.text)
    Nonce = S1["_nonce"]
    BaisongId = S1["customAccountPointLottery"]["items"][1]["id"]
    BaipiaoId = S1["customAccountPointLottery"]["items"][2]["id"]
    SteamZgSign(Cookies,Nonce)
    SteamZgLottery(Cookies,Nonce,BaisongId)
    SteamZgLottery(Cookies,Nonce,BaisongId)
    SteamZgLottery(Cookies,Nonce,BaipiaoId)
    SteamZgLottery(Cookies,Nonce,BaipiaoId)




CK=SteamZgLogin("kingkit@qq.com","123456789a")
SteamZgGetNonce(CK)
