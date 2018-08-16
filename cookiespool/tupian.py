#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from io import BytesIO
from PIL import Image

USERNAME='sha118440740@163.com'
PASSWORD='wiw120946'
op=webdriver.ChromeOptions()
op.add_argument('--headless')

class CrackWeiboSlide():
    def __init__(self):
        self.url='https://passport.weibo.cn/signin/login'
        self.browser=webdriver.Chrome(chrome_options=op)
        self.wait=WebDriverWait(self.browser,20)
        self.username=USERNAME
        self.password=PASSWORD

    def __del__(self):
        self.browser.close()

    def open(self):
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(1)
        submit.click()

    def get_position(self):
        try:
            img=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'patt-shadow')))
        except TimeoutException:
            print('未出现验证码')
            self.open()
        time.sleep(2)
        location=img.location
        size=img.size
        top,bottom,left,right=location['y'],location['y']+size['height'],location['x'],location['x']+size['width']
        return (top,bottom,left,right)

    def get_screenshot(self):
        screenshot=self.browser.get_screenshot_as_png()
        screenshot=Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self,name='captcha.png'):
        top,bottom,left,right=self.get_position()
        print('验证码位置',top,bottom,left,right)
        screenshot=self.get_screenshot()
        captcha=screenshot.crop((left,top,right,bottom))
        captcha.save(name)
        return captcha

    def main(self):
        count=0
        while True:
            self.open()
            self.get_image(str(count)+'.png')
            count+=1

if __name__=='__main__':
    crack=CrackWeiboSlide()
    crack.main()

