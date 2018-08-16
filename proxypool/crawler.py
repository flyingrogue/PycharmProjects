#!/usr/bin/env python
# _*_ coding:utf-8 _*_

'''
获取模块: 需要定时在各大代理网站抓取代理
'''

import requests
from requests.exceptions import ConnectionError
import json
import re
from pyquery import PyQuery as pq

#利用元类获取所有以crawl开头的方法名称,并将其定义成一个属性
class ProxyMetaclass(type):
    def __new__(cls, name,bases,attrs):
        count=0
        attrs['__CrawlFunc__']=[]
        #参数attrs中包含额类的方法信息
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    #执行以crawl开头的方法,将得到的代理以列表形式返回
    def get_proxies(self,callback):
        proxies=[]
        #eval()函数执行字符串表达式并返回结果
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取代理',proxy)
            proxies.append(proxy)
        return proxies

    #抓取代理网站
    def get_page(self,url,options={}):
        base_headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/67.0.3396.99 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        headers=dict(base_headers,**options)
        print('正在抓取',url)
        try:
            res=requests.get(url,headers=headers)
            print('抓取成功',url,res.status_code)
            if res.status_code==200:
                return res.text
        except ConnectionError:
            print('抓取失败',url)
            return None

    #获取代理66
    def crawl_daili66(self,page_count=4):
        start_url='http://www.ip66.cn/{}.html'
        urls=[start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print('Crawling',url)
            html=self.get_page(url)
            if html:
                doc=pq(html)
                trs=doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip=tr.find('td:nth-child(1)').text()
                    port=tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])

    #获取代理goubanjia
    def crawl_goubanjia(self):
        start_url='http://www.goubanjia.com/'
        html=self.get_page(start_url)
        if html:
            doc=pq(html)
            tds=doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield ''.join(td.text().split())

    #获取代理181
    def crawl_ip181(self):
        start_url='http://www.ip181.com'
        html=self.get_page(start_url)
        if html:
            js=json.loads(html)
            results=js.get('RESULT')
            for result in results:
                ip=result.get('ip')
                port=result.get('port')
                yield ':'.join([ip,port])


    #获取快代理
    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = self.get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    #获取代理3366
    def crawl_ip3366(self):
        for i in range(1, 4):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = self.get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    #获取西刺代理
    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWR'
                          'jZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9B'
                          'jsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = self.get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    #获取代理海
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = self.get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    #获取89代理
    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        html = self.get_page(start_url)
        if html:
            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
            ip_ports = find_ips.findall(html)
            for address_port in ip_ports:
                yield address_port

    #获取无忧代理
    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/63.0.3239.108 Safari/537.36',
        }
        html = self.get_page(start_url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

