#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
from lxml import etree
from pyquery import PyQuery as pq


keyword=input('请输入城市:')
for i in range(1,2):
    url='http://travel.qunar.com/travelbook/list/'+keyword+'/hot_heat/'+str(i)+'.htm'
    headers={
        'Host':'travel.qunar.com',
        'Upgrade - Insecure - Requests':'1',
        'User - Agent':'Mozilla / 5.0(Windows NT 6.3;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.99Safari / 537.36'
    }
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.text)
    lis=html.xpath('/html/body/div[2]/div/div[2]/ul/li')
    for li in lis:
        url='http://travel.qunar.com'+li.xpath('./h2/a/@href')[0]
        res=requests.get(url,headers=headers)
        doc=pq(res.text)
        title=doc('.user_info #booktitle').text()
        author=doc('.fix_box .head a').text()
        howlong=doc('#main_box .howlong p').text()
        howmuch=doc('#main_box .howmuch p').text()
        print('-'*100)
        print(title,author,howlong,howmuch)
        print(doc('#tpl_1').text())
        # divs=doc('#tpl_1 .e_day').items()
        # for div in divs:
        #     h1=div.find('.period_hd').text()
        #     print('-'*10,h1)
        #     items=div.find('.period_ct .b_poi_info').items()
        #     for item in items:
        #         h2=item.find('.top h5 .b_poi_title_box').text()
        #         print(h2)
        #         content=item.find('.bottom .imglst .text').text()
        #         print('-'*5,content)

