# coding : UTF-8
import urllib.request
import time
from selenium import webdriver
from datetime import datetime

# ドライブ位置設定
driver_path = "driver/chromedriver"

# 接続先のurl指定
url = 'http://dedama.me/kc_chuo/'

# クロームのオプションを保存するオブジェクト追加
options = webdriver.ChromeOptions()

# 画面を浮かばずに作動
#options.add_argument('--headless')
#driver = webdriver.Chrome(driver_path, options=options)

# 保存しておいたChrome driver呼び出し(ver.78対応)
driver = webdriver.Chrome(driver_path)

# ブラウザ立ち上げ
driver.get(url)

# 5秒待ち
time.sleep(5)

# ファイルセーブ用のファイル名指定
nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# 全体的なページのソースをdownloadページに保存
with open('download/test_'+nowtime+'.html','w',encoding='utf-8') as f:
	f.write(driver.page_source)


# 終了
driver.quit()
