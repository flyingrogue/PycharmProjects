#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
import time

browser=webdriver.Chrome()
browser.get('https://www.taobao.com')
input=browser.find_element_by_id('q')
input.send_keys('北欧床')
#input.send_keys(Keys.ENTER)
botton=browser.find_element_by_css_selector('.btn-search')
botton.click()
wait=WebDriverWait(browser,10)
for i in range(1,2):
    input=browser.find_element_by_css_selector('.input.J_Input')
    input.clear()
    input.send_keys(i)
    botton=browser.find_element_by_css_selector('.btn.J_Submit')
    botton.click()
    wait.until(EC.presence_of_element_located((By.ID,'mainsrp-itemlist')))
    page=browser.page_source
    html=etree.HTML(page)
    items=html.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
    for item in items:
        result={}
        shopname=item.xpath('.//div[2]/div[3]/div[1]/a//text()')
        result['shopname']=''.join(shopname).strip()
        result['location']=item.xpath('.//div[@class="location"]/text()')[0]
        title=item.xpath('.//a[@class="J_ClickStat"]//text()')
        result['title']=''.join(title).strip()
        result['price']=item.xpath('.//div[2]/div[1]/div[1]/strong/text()')[0]
        deal=item.xpath('.//div[@class="deal-cnt"]/text()')
        if deal:
            result['deal']=deal[0]
        result['href']='https:'+item.xpath('.//a[@class="J_ClickStat"]/@href')[0]
        print(result)
    time.sleep(1)

