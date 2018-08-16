#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import requests
from requests import Session
from requests import ConnectionError,ReadTimeout
from db import RedisQueue
from mysql import Mysql
from mongodb import MongoDB
from request import WeixinRequest
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from config import *

class Spider():
    count=1
    base_url='http://weixin.sogou.com/weixin'
    proxypool_url=PROXYPOOL_URL
    keyword=KEYWORD
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'ABTEST=5|1532314313|v1; SUID=B50142311F2D940A000000005B5542C9; weixinIndexVisited=1;'
                 ' ppinf=5|1532326946|1533536546|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlQTUlQkQlRTYl'
                 'ODMlQjN8Y3J0OjEwOjE1MzIzMjY5NDZ8cmVmbmljazoxODolRTUlQTUlQkQlRTYlODMlQjN8dXNlcmlkOjQ0Om85dDJsdU1zcUd'
                 'LUkZhNFhHUFZDY05WcVg4Nk1Ad2VpeGluLnNvaHUuY29tfA; pprdig=l7bPSuHEX2Dw59St_Hr2jsd9yOCiEQg-SINIWoJwCTf'
                 '2NQ4D7oVXLanLnrvYbyRy_v1-ELWd_AxHVeBrAv0m6MNA_sLeRYd4rZK6oGkl7MuMcIwLsO1LNymIEDQyzrO5EKUiD6XDGKr5nS'
                 'v3-FK2IT2yKUXHdv_CHpYLO507QTc; sgid=20-36194065-AVtVdCKIibiaGVBqLwI9ItDZU; UM_distinctid=164c81479f'
                 '755c-0932f36bc02d29-5b193613-144000-164c81479f8640; CNZZDATA1261666818=1219770327-1532362355-%7C153'
                 '2362355; IPLOC=CN3202; SUID=3E0442313108990A000000005B56963C; SUV=00771DED3142043E5B56963D70C16776;'
                 ' sct=5; SNUID=142E681B2B2F5B9FDD32825E2B9C0829; JSESSIONID=aaatZ36oaO6QKh8i9qHsw; ppmdig=1532422395'
                 '00000000ab72fee141c5ddb0e58074d76e7065',
        'Host':'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                     ' Chrome/67.0.3396.99 Safari/537.36'
    }
    session=Session()
    queue=RedisQueue()
    mysql=Mysql()
    mongo=MongoDB()

    #初始化工作
    def start(self):
        #全局更新headers
        self.session.headers.update(self.headers)
        start_url=self.base_url+'?'+urlencode({'query':self.keyword,'type':2})
        weixin_request=WeixinRequest(url=start_url,callback=self.parse_index,need_proxy=True)
        #调度第一个请求
        self.queue.add(weixin_request)

    #开始调度请求
    def schedule(self):
        while not self.queue.empty():
            weixin_request=self.queue.pop()
            callback=weixin_request.callback
            print('Schedule',weixin_request.url)
            response=self.send_request(weixin_request)
            if response and response.status_code==200:
                results=list(callback(response))
                if results:
                    for result in results:
                        print('New Result',result)
                        if isinstance(result,WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result,dict):
                            #self.mysql.insert(result)
                            self.mongo.insert(result)
                else:
                    print('获得的页面不正确')
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    #执行请求
    def send_request(self,weixin_request):
        try:
            if weixin_request.need_proxy:
                proxy=self.get_proxy()
                if proxy:
                    proxies={
                        'http':'http://'+proxy,
                        'https':'https://'+proxy
                    }
                    return self.session.send(weixin_request.prepare(),
                                             timeout=weixin_request.timeout,allow_redirects=False,proxies=proxies)
            #注意此处一定要允许重定向,否则状态码为301
            return self.session.send(weixin_request.prepare(),timeout=weixin_request.timeout,allow_redirects=True)
        except (ConnectionError,ReadTimeout) as e:
            print(e.args)
            return False

    #从代理池获取代理
    def get_proxy(self):
        try:
            response=requests.get(self.proxypool_url)
            if response.status_code==200:
                print('Get Proxy',response.text)
                return response.text
            return None
        except ConnectionError:
            return None

    #解析索引页
    def parse_index(self,response):
        doc=pq(response.text)
        items=doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url=item.attr('href')
            weixin_request=WeixinRequest(url=url,callback=self.parse_detail)
            yield weixin_request
        next=doc('#sogou_next').attr('href')
        if self.count<MAX_PAGE:
            if next:
                self.count+=1
                url=self.base_url+next
                weixin_request=WeixinRequest(url=url,callback=self.parse_index,need_proxy=True)
                yield weixin_request


    #解析详情页
    def parse_detail(self,response):
        doc=pq(response.text)
        data={
            'title':doc('.rich_media_title').text(),
            'content':''.join((doc('.rich_media_content').text()).split()),
            'date':doc('#post-date').text(),
            'nickname':doc('#js_profile_qrcode > div > strong').text(),
            'wechat':doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        yield data

    #错误处理
    def error(self,weixin_request):
        weixin_request.fail_time += 1
        print('Request Failed',weixin_request.fail_time,'Times',weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(weixin_request)


