#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymysql
import pymongo

chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser=webdriver.Chrome(chrome_options=chrome_options)
#browser=webdriver.Chrome()
#browser=webdriver.PhantomJS()
wait=WebDriverWait(browser,10)
KEYWORD='iPhone'
MAXPAGE=5

def get_page(page):
    print('正在爬取第',page,'页')
    try:
        url='https://s.taobao.com/search?q='+quote(KEYWORD)
        browser.get(url)
        if page>1:
            input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form>input')))
            submit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form>span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        return browser.page_source
    except TimeoutException:
        get_page(page)

def get_products(page_source):
    doc=pq(page_source)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product={
            'title':''.join(item.find('.title').text().split()),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
            'price':item.find('.price').text().split('\n')[1],
            'deal':item.find('.deal-cnt').text(),
            'href':'https:'+item.find('.title .J_ClickStat').attr('href')
        }
        yield product

def open_mysql():
    db = pymysql.connect(host='localhost', user='root', password='ljb1994917', port=3306, db='taobao')
    cursor = db.cursor()
    sql='CREATE TABLE IF NOT EXISTS products(id INT AUTO_INCREMENT PRIMARY KEY,title VARCHAR(100) NOT NULL,' \
        'shop VARCHAR(100) NOT NULL,location VARCHAR(100) NOT NULL,price VARCHAR(100) NOT NULL,deal VARCHAR(100),' \
        'href VARCHAR(255) NOT NULL)'
    cursor.execute(sql)
    return db

def to_mysql(db,product):
    cursor=db.cursor()
    sql='INSERT INTO products(title,shop,location,price,deal,href) values (%s,%s,%s,%s,%s,%s)'
    try:
       cursor.execute(sql,tuple(product.values()))
       db.commit()
    except:
        db.rollback()

def open_mongodb():
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.taobao
    collection=db.products
    return collection

if __name__=='__main__':
    #db=open_mysql()
    collection=open_mongodb()
    for i in range(1,MAXPAGE+1):
        page_source=get_page(i)
        for product in get_products(page_source):
            print(product)
            #to_mysql(db,product)
            collection.insert_one(product)
    #db.close()
