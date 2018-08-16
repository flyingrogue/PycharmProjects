#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
from requests import Session
url='https://m.weibo.cn/'
headers={
        'Host':'m.weibo.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                     ' Chrome/67.0.3396.99 Safari/537.36'
}
proxy='194.44.12.55:8080'
proxies={
    'http':'http://'+proxy,
    'https':'https://'+proxy
}
requests.adapters.DEFAULT_RETRIES = 5
s=requests.Session()
s.keep_alive=False
res=s.get(url,proxies=proxies,allow_redirects=False)
print(res.status_code)
print(res.text)