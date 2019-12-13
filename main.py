# coding : UTF-8
import urllib.request
import time
import main_func as main_func
import MySQLdb

from selenium import webdriver
from datetime import datetime
#　絶対パスを簡単に取得敵るようにする。
from pathlib import Path


# ドライブ位置設定
driver_path = "driver/chromedriver"

# 接続先のurl指定
url = 'http://dedama.me/kc_chuo/'

#データベース接続情報
conn = MySQLdb.connect(
 unix_socket = 'C:/xampp/mysql/mysql.sock',
 user='root1',
 passwd='root1',
 host='localhost',
 db='pachinko')

# クロームのオプションを保存するオブジェクト追加
options = webdriver.ChromeOptions()

# ファイル保存用のファイル名指定
nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
nowday = datetime.now().strftime("%Y_%m_%d")

# 画面を浮かばずに作動
options.add_argument('--headless')
driver = webdriver.Chrome(driver_path, options=options)

# 保存しておいたChrome driver呼び出し(ver.78対応)
driver = webdriver.Chrome(driver_path)

# テーブル保存先の名前
table_dir_name = nowday

# テーブル情報収納ディレクトリ
table_dir = main_func.make_table_folder_get_path(table_dir_name,Path)

# カーソルを取得
cur = conn.cursor()

# ブラウザ立ち上げ
driver.get(url)

# 5秒待ち
time.sleep(5)

# frame変更
main_func.switch_driver(driver)

# データテーブル作成
main_func.make_database(cur)

# 一応テストようの
main_func.get_table_test(driver, table_dir, nowtime, Path, time)


# sqlをコミット
conn.commit()
# 終了
driver.quit()
