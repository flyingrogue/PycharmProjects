from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from io import BytesIO
from PIL import Image

EMAIL='qwer'
PASSWORD='asdf'

class TestSlide():
    def __init__(self,browser,wait):
        self.url='https://account.geetest.com/login'
        self.browser=browser
        self.wait=wait
        self.email=EMAIL
        self.password=PASSWORD

    def __del__(self):
        self.browser.close()

    def get_geetest_botton(self):
        button=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')))
        return button

    def get_position(self):
        img=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_canvas_img')))
        time.sleep(1)
        location=img.location
        size=img.size
        top,bottom,left,right=location['y'],location['y']+size['height'],location['x'],location['x']+size['width']
        return (top,bottom,left,right)

    def get_geetest_image(self,name='captcha.png'):
        top,bottom,left,right=self.get_position()
        print('验证码位置',top,bottom,left,right)
        time.sleep(0.6)
        screenshot=self.browser.get_screenshot_as_png()
        screenshot=Image.open(BytesIO(screenshot))
        captcha=screenshot.crop((left,top,right,bottom))
        captcha.save(name)
        return captcha

    def get_slider(self):
        slider=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_slider_button')))
        return slider

    def is_pixel_equal(self,image1,image2,x,y):
        pixel1=image1.load()[x,y]
        pixel2=image2.load()[x,y]
        threshold=60
        if abs(pixel1[0]-pixel2[0]) < threshold and abs(pixel1[1]-pixel2[1]) < threshold and\
            abs(pixel1[2]-pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self,image1,image2):
        left=60
        for i in range(left,image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1,image2,i,j):
                    left=i
                    return left
        return left


    def get_track(self,distance):
        track=[]
        current=0
        mid=distance*4/5
        v=0
        t=0.2
        while current < distance:
            if current < mid:
                a=2
            else:
                a=-3
            v0=v
            v=v0+a*t
            move=v0*t + 1/2*a*t*t
            current+=move
            track.append(round(move))
        return track

    def move_to_gap(self,slider,track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        ActionChains(self.browser).release().perform()

    def open(self):
        self.browser.get(self.url)
        email=self.wait.until(EC.presence_of_element_located((By.ID,'email')))
        password=self.wait.until(EC.presence_of_element_located((By.ID,'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def is_success(self):
        try:
            return bool(WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_success_btn'))))
        except TimeoutException:
            return False

    def main(self):
        self.open()
        button=self.get_geetest_botton()
        button.click()
        image1=self.get_geetest_image('captcha1.png')
        slider=self.get_slider()
        slider.click()
        image2=self.get_geetest_image('captcha2.png')
        gap=self.get_gap(image1,image2)
        print('缺口位置',gap)
        gap-=6
        track=self.get_track(gap)
        print('滑动轨迹',track)
        self.move_to_gap(slider,track)
        if self.is_success():
            print('success')
        else:
            print('fail')


if __name__=='__main__':
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser=webdriver.Chrome(options=chrome_options)
    wait=WebDriverWait(browser,10)
    a=TestSlide(browser,wait)
    a.main()






