#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import json
import re
import pymysql
import xml.etree.ElementTree as et
from urllib.parse import urlencode
import pymongo

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
                 ' (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def get_schoolid(schoolname):
    headers['Referer']='https://gkcx.eol.cn/soudaxue/queryschool.html?&keyWord1='+str(schoolname.encode('utf-8'))
    parmas = {
        'messtype': 'jsonp',
        'callback': 'jQuery18305791364386826103_1530933687342',
        'province': '','page': '1', 'size': '30',
        'keyWord1': schoolname,
        'schoolprop': '', 'schoolflag': '', 'schoolsort': '', 'schoolid': '', 'schooltype': '',
        '_': '1530933687541'
    }
    url = 'https://data-gkcx.eol.cn/soudaxue/queryschool.html?' + urlencode(parmas)
    res = requests.get(url, headers=headers, )
    # print(res.text) #得到的不是一个合法的json数据,被();包围着,需进一步处理,可用正则或split分割
    text = ((res.text).split(');', 1)[0]).split('(', 1)[1]
    school_list = json.loads(text).get('school')
    return [{'schoolid':i['schoolid'],'schoolname':i['schoolname']} for i in school_list]

def get_provinceid(province):
    url = 'https://static.eol.cn/gkcx/static/js/commonParams.js'
    res = requests.get(url)
    #得到的不知是啥格式数据,只好用正则提取了
    temp = (res.text).split(';', 1)[0]
    a = re.findall('GH(.*)//JLNQ(.*)//STXYZ(.*)}', temp, re.S)[0]
    dict = {}
    for i in range(3):
        for j in a[i].split(','):
            b = re.findall('"(.*?)"', j)
            if b:
                dict[b[0]] = b[1]
    return dict[province]

def get_keleiid(kelei):
    dict={'理科':'10035','文科':'10034'}
    return dict[kelei]

def get_xml(schoolid,provinceid,keleiid):
    headers['Referer']='https://gkcx.eol.cn/schoolhtm/schoolTemple/school' + schoolid + '.htm'
    headers['X-Requested-With']='XMLHttpRequest'
    url = 'https://gkcx.eol.cn/commonXML/schoolSpecialPoint/schoolSpecialPoint' + schoolid + '_' + provinceid + '_' + keleiid + '.xml'
    res = requests.get(url, headers=headers)
    #得到的是xml格式数据,用xml.etree.ElementTree来提取
    res.encoding = 'utf-8'
    if res.url == url:
        areapionts=et.fromstring(res.text)
        for areapiont in areapionts:
            item={}
            item['year']=areapiont.find('year').text
            item['specialname']=areapiont.find('specialname').text
            item['maxfs']=areapiont.find('maxfs').text
            item['varfs']=areapiont.find('varfs').text
            item['minfs']=areapiont.find('minfs').text
            item['pc']=areapiont.find('pc').text
            item['stype']=areapiont.find('stype').text
            yield item

def open_mysql(school,province):
    db = pymysql.connect(host='localhost', user='root', password='ljb1994917', port=3306, db='gkcx')
    cursor = db.cursor()
    tablename=school+province
    #此处表名是个变量,利用%s传递,auto increment可使id自增
    sql = 'CREATE TABLE IF NOT EXISTS %s'%tablename + '(id INT AUTO_INCREMENT,学校 VARCHAR(100) NOT NULL,年份 VARCHAR(100) NOT NULL,' \
         '专业名称 VARCHAR(100) NOT NULL,最高分 VARCHAR(100) NOT NULL,平均分 VARCHAR(100) NOT NULL,' \
         '最低分 VARCHAR(100) NOT NULL,录取批次 VARCHAR(100) NOT NULL,科类 VARCHAR(100) NOT NULL,PRIMARY KEY (id))'
    cursor.execute(sql)
    return db

def to_mysql(school,province,item,db):
    tablename=school+province
    cursor=db.cursor()
    sql='INSERT INTO %s'%tablename + '(学校,年份,专业名称,最高分,平均分,最低分,录取批次,科类) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql,(item['school'],item['year'],item['specialname'],item['maxfs'],item['varfs'],
                            item['minfs'],item['pc'],item['stype']))
        db.commit()
    except:
        db.rollback()

def open_mongodb(school,province):
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.gaokao
    collection=db[school+province]
    return collection

if __name__=='__main__':
    school=input('Please enter the school name:')
    schoolinfos=get_schoolid(school)
    print('共检索到{}个高校:{}'.format(len(schoolinfos),[info['schoolname'] for info in schoolinfos]))
    province=input('Please enter the province name:')
    provinceid=get_provinceid(province)
    kelei=input('Please enter the kelei:')
    keleiid=get_keleiid(kelei)
    #db=open_mysql(school,province)
    collection=open_mongodb(school,province)
    for info in schoolinfos:
        schoolid=info['schoolid']
        schoolname=info['schoolname']
        for item in get_xml(schoolid,provinceid,keleiid):
            item['school']=schoolname
            collection.insert_one(item)
            #print(item)
            #to_mysql(school,province,item,db)
    #db.close()


