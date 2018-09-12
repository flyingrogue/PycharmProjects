from cookiespool.slide import TestSlide
from cookiespool.click import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import json

class XueqiuCookies():
    def __init__(self,username,password,browser):
        self.url='https://xueqiu.com'
        self.browser=browser
        self.username=username
        self.password=password
        self.wait=WebDriverWait(self.browser,10)


    def login_successfully(self):
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'user-name'))))
        except TimeoutException:
            return False

    def is_slide(self):
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img'))))
        except TimeoutException:
            return False

    # def is_click(self):
    #     try:
    #         return bool(
    #             WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_wrap'))))
    #     except TimeoutException:
    #         return False

    def process_slide(self):
        testslide=TestSlide(self.browser,self.wait)
        image1 = testslide.get_geetest_image('captcha1.png')
        slider = testslide.get_slider()
        slider.click()
        image2 = testslide.get_geetest_image('captcha2.png')
        gap = testslide.get_gap(image1, image2)
        print('缺口位置', gap)
        gap -= 6
        track = testslide.get_track(gap)
        print('滑动轨迹', track)
        testslide.move_to_gap(slider, track)

    def process_click(self):
        testclick=TestClick(self.browser,self.wait)
        testclick.main()

    def open(self):
        self.browser.get(self.url)
        login=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'nav__login__btn')))
        login.click()
        username=self.wait.until(EC.presence_of_element_located((By.NAME,'username')))
        password=self.wait.until(EC.presence_of_element_located((By.NAME,'password')))
        botton=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'modal__login__btn')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(0.5)
        botton.click()

    def main(self):
        self.open()
        if self.login_successfully():
            cookies=self.browser.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        elif self.is_slide():
            self.process_slide()
            if self.login_successfully():
                cookies=self.browser.get_cookies()
                return {
                    'status': 1,
                    'content': cookies
                }
            else:
                return {
                    'status': 2,
                    'content': '登录失败'
                }
        else:
            self.process_click()
            if self.login_successfully():
                cookies=self.browser.get_cookies()
                return {
                    'status': 1,
                    'content': cookies
                }
            else:
                return {
                    'status': 2,
                    'content': '登录失败'
                }


if __name__=='__main__':
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser=webdriver.Chrome(options=chrome_options)
    result=XueqiuCookies('18516710917','',browser).main()
    cookies=result.get('content')
    dict={}
    for cookie in cookies:
        dict[cookie['name']] = cookie['value']
    print(dict)



