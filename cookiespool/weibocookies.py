#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
import time
from io import BytesIO
from PIL import Image
from os import listdir
from os.path import abspath, dirname

TEMPLATES_FOLDER=dirname(abspath(__file__)) + '/templates/'


#模拟登陆微博,获取cookies
class WeiboCookies():
    def __init__(self,username,password,browser):
        self.url='https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
        self.browser=browser
        self.wait=WebDriverWait(self.browser,20)
        self.username=username
        self.password=password

    #打开网页输入用户名密码并点击
    def open(self):
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        username=self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password=self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit=self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        time.sleep(1)
        submit.click()

    #判断是否密码错误
    def password_error(self):
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            return False

    #判断是否登陆成功
    def login_successfully(self):
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile'))))
        except TimeoutException:
            return False

    #获取验证码位置
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

    #获取网页截图
    def get_screenshot(self):
        screenshot=self.browser.get_screenshot_as_png()
        screenshot=Image.open(BytesIO(screenshot))
        return screenshot

    #获取验证码图片
    def get_image(self,name='captcha.png'):
        top,bottom,left,right=self.get_position()
        print('验证码位置',top,bottom,left,right)
        screenshot=self.get_screenshot()
        captcha=screenshot.crop((left,top,right,bottom))
        return captcha

    #判断两个像素是否相同
    def is_pixel_equal(self, image1, image2, x, y):
        #取两个图片的像素点
        pixel1=image1.load()[x, y]
        pixel2=image2.load()[x, y]
        threshold=20
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    #识别相似验证码
    def same_image(self, image, template):
        #相似度阈值
        threshold=0.99
        count=0
        for x in range(image.width):
            for y in range(image.height):
                #判断像素是否相同
                if self.is_pixel_equal(image, template, x, y):
                    count+=1
        result=float(count) / (image.width * image.height)
        print(result)
        if result > threshold:
            print('成功匹配')
            return True
        return False

    #将获取到验证码图片与图库匹配
    def detect_image(self, image):
        for template_name in listdir(TEMPLATES_FOLDER):
            print('正在匹配', template_name)
            template=Image.open(TEMPLATES_FOLDER + template_name)
            if self.same_image(image, template):
                # 返回顺序
                numbers=[int(number) for number in list(template_name.split('.')[0])]
                print('拖动顺序', numbers)
                return numbers


    #根据顺序拖动
    def move(self, numbers):
        #获得四个按点
        try:
            circles=self.browser.find_elements_by_css_selector('.patt-wrap .patt-circ')
            dx=dy=0
            for index in range(4):
                circle=circles[numbers[index] - 1]
                #如果是第一次循环
                if index==0:
                    #点击第一个按点
                    ActionChains(self.browser) \
                        .move_to_element_with_offset(circle, circle.size['width'] / 2, circle.size['height'] / 2) \
                        .click_and_hold().perform()
                else:
                    #小幅移动次数
                    times=30
                    #拖动
                    for i in range(times):
                        ActionChains(self.browser).move_by_offset(dx / times, dy / times).perform()
                        time.sleep(1 / times)
                #如果是最后一次循环
                if index==3:
                    #松开鼠标
                    ActionChains(self.browser).release().perform()
                else:
                    #计算下一次偏移
                    dx=circles[numbers[index + 1] - 1].location['x'] - circle.location['x']
                    dy=circles[numbers[index + 1] - 1].location['y'] - circle.location['y']
        except:
            return False

    #获取cookies入口
    def main(self):
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        #如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies=self.browser.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        #获取验证码图片
        image=self.get_image('captcha.png')
        numbers=self.detect_image(image)
        self.move(numbers)
        if self.login_successfully():
            cookies=self.browser.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 3,
                'content': '登录失败'
            }


if __name__=='__main__':
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser=webdriver.Chrome(chrome_options=chrome_options)
    result=WeiboCookies('rongluy4730606@163.com','hgg033291',browser).main()
    print(result)



