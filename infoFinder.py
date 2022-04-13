import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pandas as pd
import re

emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

option = webdriver.ChromeOptions()
#option.add_argument("--headless")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                          options=option)


def getInfo(url):
    info = {}
    driver.get(url)
    time.sleep(1)

    # 标题
    try:
        try:
            title = driver.find_element(by=By.CSS_SELECTOR, value="div[id='viewbox_report'] > h1 > span")
            title = title.text
        except: # 视频是否参加活动会影响title的class，如果他变了，报错了，可以except这里写下改变之后的class
            # 这样如果他只变一次，是可以处理的。
            title = driver.find_element(by=By.TAG_NAME, value="div[id='viewbox_report'] > h1")
            # remove all non-utf-8 characters such as emojis
            title = title.get_attribute(title)
            #title = title.decode('utf-8', 'ignore').encode("utf-8")

        title = emoji_pattern.sub(r'', title)

        info['title'] = title

        like = driver.find_element(by=By.TAG_NAME, value="span[class='like']")
        info['like'] = like.text
        coin = driver.find_element(by=By.TAG_NAME, value="span[class='coin']")
        info['coin'] = coin.text
        collect = driver.find_element(by=By.TAG_NAME, value="span[class='collect']")
        info['collect'] = collect.text
        share = driver.find_element(by=By.TAG_NAME, value="span[class='share']")
        info['share'] = share.text

        # 视频信息
        view = driver.find_element(by=By.CSS_SELECTOR, value="span.view").text
        view = view.replace('播放 ·', '')
        dm = driver.find_element(by=By.CSS_SELECTOR, value="span.dm").text
        dm = dm.replace('总弹幕数', '')
        upload_date = driver.find_element(by=By.CSS_SELECTOR, value="div.video-data > span:nth-child(3)").text
        upload_date = upload_date.split(' ')[0]
        info['view'] = view
        info['dm'] = dm
        info['upload_date'] = upload_date

    except:
        print('========== An error was raised')
        info['title'] = 'An error was raised'
        info['url'] = url
        time.sleep(60)

    return info
'''    
    
'''
