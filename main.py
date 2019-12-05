# coding : UTF-8
import urllib.request
import time
from selenium import webdriver
from datetime import datetime

# ドライブ位置設定
driver_path = "driver/chromedriver"

# 接続先のurl指定
url = 'http://dedama.me/kc_chuo/'

options = webdriver.ChromeOptions()

# 画面を浮かばずに作動
#options.add_argument('--headless')
#driver = webdriver.Chrome(driver_path, options=options)

driver = webdriver.Chrome(driver_path)

driver.get(url)

time.sleep(5)
nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

with open('download/test_'+nowtime+'.html','w') as f:
	f.write(driver.page_source)


time.sleep(5)
driver.quit()
