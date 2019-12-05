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
options.add_argument('--headless')
driver = webdriver.Chrome(driver_path, options=options)

# 保存しておいたChrome driver呼び出し(ver.78対応)
driver = webdriver.Chrome(driver_path)

# ブラウザ立ち上げ
driver.get(url)

# 5秒待ち
time.sleep(5)

# ファイルセーブ用のファイル名指定
nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# 全体的なページのソースをdownloadページに保存
with open('download/test_'+nowtime+'_(1).html','w',encoding='utf-8') as f:
	f.write(driver.page_source)

# frame変更
driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='contents']"))

# 全体的なページのソースをdownloadページに保存
with open('download/test_'+nowtime+'_(2).html','w',encoding='utf-8') as f:
	f.write(driver.page_source)

# 現在フレームのスクリーンショット
driver.save_screenshot('screenshot/screenshot_'+nowtime+'.png')

# テーブル取得
data_table = driver.find_element_by_id("data-block")

#　テーブル目録保存
with open('table/table_'+nowtime+'.html','w',encoding='utf-8') as f:
	f.write(data_table.get_attribute('innerHTML'))

# for文でテーブルごとのリンクに入る

# link先のスクリーンショットを撮る

# 終了
driver.quit()
