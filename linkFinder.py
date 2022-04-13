from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pandas as pd
import os
from general import *


option = webdriver.ChromeOptions()
#option.add_argument("--headless")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                          options=option)
PROJECT_NAME = 'blizzard_games'
GAME_NAMES = ['暗黑破坏神', '星际争霸', '暗黑破坏神II', '魔兽争霸',
              '冰封王座', '魔兽世界', '炉石传说', '风暴英雄',
              'X战警前传：金刚狼', "天诛系列", '命运战士', '变形金刚2：卷土重来', '吉他英雄',
              '虐杀原形', '使命召唤', '命运2']

data_folder = 'url_list'
create_project_dir(data_folder)

max_page = 34
for game_name in GAME_NAMES:
    print('Gathering links for ' + game_name)
    urls_filename = game_name + '_urls.txt'
    path = os.path.join(data_folder, urls_filename)
    f = open(path, 'w')

    for page in range(max_page):
        o_num = (page - 1) * 30
        if page == 1:
            url = "https://search.bilibili.com/all?keyword=" + game_name + "&from_source=webtop_search&spm_id_from=333.1007"
        else:
            url = "https://search.bilibili.com/all?keyword=" + game_name + "&from_source=webtop_search&spm_id_from=333.1007&page=" + str(page) + "&" + str(o_num) +"=30"
        driver.get(url)
        time.sleep(1)
        video_as = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='bili-video-card__info--right']  > a")
        for video_a in video_as:
            video_link = video_a.get_attribute('href') + '\n'
            f.write(video_link)
    f.close()