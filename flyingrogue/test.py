
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

browser=webdriver.Chrome()
try:
    browser.get('https://www.zhihu.com/explore')
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    #browser.execute_script('alert("To Bottom")')
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[1])
    browser.get('https://www.taobao.com')
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    browser.get('https://www.baidu.com')

    #input=browser.find_element_by_id('kw')
    #input.send_keys('Python')
    #input.send_keys(Keys.ENTER)
    #button=browser.find_element_by_id('su')
    #button.click()
    #wait=WebDriverWait(browser,10)
    #wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    #print(browser.current_url)
    #print(browser.get_cookies())
    #print(browser.page_source)
finally:
    #browser.close()
    pass

