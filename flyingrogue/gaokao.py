#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import re
import json
from urllib.parse import urlencode
import xml.etree.ElementTree as et


base_url='https://static.eol.cn/gkcx/static/js/commonParams.js'
res=requests.get(base_url)

temp=(res.text).split(';',1)[0]
a=re.findall('GH(.*)//JLNQ(.*)//STXYZ(.*)}',temp,re.S)[0]
dict={}
for i in range(3):
    for j in a[i].split(','):
        asd=re.findall('"(.*?)"',j)
        if asd:
            dict[asd[0]] = asd[1]

dict2={'理科':'10035','文科':'10034'}


kelei='理科'
province='江西'
school='东南大学'
#a=school.encode('utf-8')
#b=str(a)
#print(a,type(a),b,type(b))
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
                 ' (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Host':'data-gkcx.eol.cn',
    'Referer':'https://gkcx.eol.cn/soudaxue/queryschool.html?&keyWord1='+str(school.encode('utf-8'))
}
#print(headers['Referer'])
parmas={
    'messtype':'jsonp',
    'callback':'jQuery18305791364386826103_1530933687342',
    'province':'',
    'page':'1','size':'30',
    'keyWord1':school,
    'schoolprop':'','schoolflag':'','schoolsort':'','schoolid':'','schooltype':'',
    '_':'1530933687541'
}
url='https://data-gkcx.eol.cn/soudaxue/queryschool.html?'+urlencode(parmas)
res=requests.get(url,headers=headers,)
#print(res.text) #得到的不是一个合法的json数据,被();包围着,需进一步处理,可用正则或split分割
text=((res.text).split(');',1)[0]).split('(',1)[1]
school_list=json.loads(text).get('school')
for i in school_list:
    schoolid=i['schoolid']
    schoolname=i['schoolname']
    headers={
        'Referer': 'https://gkcx.eol.cn/schoolhtm/schoolTemple/school' + schoolid + '.htm',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    url='https://gkcx.eol.cn/commonXML/schoolSpecialPoint/schoolSpecialPoint'+schoolid+'_'+dict[province]+'_'+dict2[kelei]+'.xml'
    res=requests.get(url,headers=headers)
    res.encoding='utf-8'
    #a=re.findall('<year>(.*)</year>',res.text)
    #print(a)
    if res.url == url:
        areapionts=et.fromstring(res.text)
        for areapiont in areapionts:
           year=areapiont.find('year').text
           specialname=areapiont.find('specialname').text
           maxfs=areapiont.find('maxfs').text
           varfs=areapiont.find('varfs').text
           minfs=areapiont.find('minfs').text
           pc=areapiont.find('pc').text
           stype=areapiont.find('stype').text
           print([schoolname,year,specialname,maxfs,varfs,minfs,pc,stype])














