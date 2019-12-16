# coding : UTF-8
import urllib.request
import time
import main_func as main_func
import MySQLdb
import schedule
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

# カーソルを取得
cur = conn.cursor()

# データテーブル作成
main_func.make_database(cur)

def job():
	nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	nowday = datetime.now().strftime("%Y_%m_%d")
	print("現在時間"+nowtime+"作業を始めます")
	# エラーが出るまで回す
	while True:
		# ドライバー指定
		driver = webdriver.Chrome(driver_path, options=options)

		# ブラウザ立ち上げ
		driver.get(url)

		# 1秒待ち
		time.sleep(1)

		# frame変更
		main_func.switch_driver(driver)

		if main_func.get_table(driver, nowtime, nowday, Path, time, cur) == False:
			continue;

		else :
			break;
			# 情報をテーブルに入れる
	# BOTの疑い回避の為にクッキー全削除
	driver.delete_all_cookies()

	# 終了
	driver.close()

	# sqlをコミット
	# conn.commit()

	# 完了報告
	print(nowday+"の情報が保存されました。")

while True:
	job()

# 特定時間に指定関数が動くようにする
# schedule.every().day.at("08:00").do(job)

# 現在時間にちゃんと関数が動くかを表示
# while True:
# 	nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# 	nowday = datetime.now().strftime("%Y_%m_%d")
# 	print("System is operating")
# 	print("current time is : "+nowtime)
# 	schedule.run_pending()
# 	time.sleep(60)		



