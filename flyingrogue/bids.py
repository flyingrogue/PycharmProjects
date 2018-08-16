#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
from lxml import etree

url='http://www.gpa.gov.nl.ca/gs/report/GenReport.asp'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
res=requests.get(url,headers=headers)
html=etree.HTML(res.text)
hrefs=html.xpath('//*[@id="gnlwrap"]/div[3]/div/center/div[3]/center/table[1]//a/@href')
#print(hrefs)
for href in hrefs:
    url='http://www.gpa.gov.nl.ca/gs/report/'+href
    res=requests.get(url)
    html=etree.HTML(res.text)
    action=html.xpath('//*[@id="gnlwrap"]/div[3]/div/center/table//tr/td/div/table//tr/td/div/form/@action')[0]
    url='http://www.gpa.gov.nl.ca/gs/report/'+action
    data={
        'LegalAction':'Accept'
    }
    res=requests.post(url,data=data)
    #print(res.url)
    html=etree.HTML(res.text)
    time=html.xpath('//*[@id="gnlwrap"]/div[3]/div[4]/center/table//tr/td/table[8]//tr[2]/td/text()')
    #print(time[0][1:],time[1][1:])
    list=[time[0][1:],time[1][1:]]
    desc=html.xpath('//*[@id="gnlwrap"]/div[3]/div[7]/center/table//tr/td/div[1]/center/table//tr/td[2]/text()')
    #print(desc)
    list.append(desc[0])
    files=html.xpath('//*[@id="gnlwrap"]/div[3]/div[7]/center/table//tr/td//a/@href')
    if files:
        #print(files[1:])
        for file in files[1:]:
            list.append(file)
    print(list)