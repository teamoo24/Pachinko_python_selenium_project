# coding : UTF-8
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

#　絶対パスを簡単に取得敵るようにする。
from pathlib import Path

# ドライブ位置設定
driver_path = "driver/chromedriver"

# 接続先のurl指定
url = 'http://dedama.me/kc_chuo/'

# ファイル保存用のファイル名指定
nowtime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
nowday = datetime.now().strftime("%Y_%m_%d")

# クロームのオプションを保存するオブジェクト追加
options = webdriver.ChromeOptions()

# 画面を浮かばずに作動
options.add_argument('--headless')
driver = webdriver.Chrome(driver_path, options=options)

# 保存しておいたChrome driver呼び出し(ver.78対応)
driver = webdriver.Chrome(driver_path)

# テーブル保存先の名前
table_dir_name = nowday

# テーブル情報収納ディレクトリ
table_dir = None

# ページ全体のソースを取得
def get_page_source(driver, option):
	# 全体的なページのソースをdownloadページに保存
	with open('download/test_'+nowtime+option+'.html','w',encoding='utf-8') as f:
		f.write(driver.page_source)

def switch_driver(driver):
	driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='contents']"))

# 現在のスクリーンショットを撮る
def get_screenshot(driver, path):
	page_width = driver.execute_script('return document.body.scrollWidth')
	page_height = driver.execute_script('return document.body.scrollHeight')

	driver.set_window_size(page_width, page_height)	

	driver.save_screenshot(path)

# テーブル情報を保存するメインディレクトリ指定
def make_table_folder():
	
	# 保存先フォルダ名
	table_dir_path = Path("table/"+table_dir_name)

	# 今日の日付のフォルダーを生成(存在してる場合スキップ)
	table_dir_path.mkdir(exist_ok=True)

	global table_dir 

	table_dir= str(table_dir_path.resolve())

# テーブルの情報を保存
# driver : 現在のdriverの情報
# data_table : メインテーブル
def get_table(driver):

	# テーブル取得
	data_table = driver.find_element_by_id("data-block")

	# テーブル目録保存
	with open(table_dir+'/'+nowtime+'.html','w',encoding='utf-8') as f:
		f.write(data_table.get_attribute('innerHTML'))

	# trのリストを取得
	trs = data_table.find_elements(By.TAG_NAME, "tr")

	for i in range(1,len(trs)):
		
		if(i > 1):
			switch_driver(driver)
		get_page_source(driver, str(i))
		data_table = driver.find_element_by_id("data-block")
		
		# trのリストを取得
		trs = data_table.find_elements(By.TAG_NAME, "tr")

		tds = trs[i].find_elements(By.TAG_NAME, "td")

		for j in range(0, len(tds)+1):

			try:
				if(j > 1):
					switch_driver(driver)
				data_table = driver.find_element_by_id("data-block")

				# trのリストを取得
				trs = data_table.find_elements(By.TAG_NAME, "tr")
				tds = trs[i].find_elements(By.TAG_NAME, "td")


				for a in driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr["+str(i)+"]/td["+str(j)+"]/a"):
					
	    			# for文でテーブルごとのリンクに入る
					kishu_name = str(a.get_attribute('innerHTML'))
					print(kishu_name+"を作業")
		   			# 保存先フォルダ名
					kishu_path = Path(table_dir+"/"+kishu_name)

					# 今日の日付のフォルダーを生成(存在してる場合スキップ)
					kishu_path.mkdir(exist_ok=True)

					a.click()

					# 出玉テーブルのスクリーンショット
					get_screenshot(driver, str(kishu_path)+'/screenshot_'+nowtime+'.png')
					
					# 本のページに戻る
					driver.back()

					time.sleep(2)

			except NoSuchElementException:
				print("get Error")
				get_page_source(driver,"error")

# ブラウザ立ち上げ
driver.get(url)

# 5秒待ち
time.sleep(5)

# frame変更
switch_driver(driver)

# 現在フレームのスクリーンショット
# driver.save_screenshot('screenshot/screenshot_'+nowtime+'.png')

# テーブル情報保存フォルダー作成
make_table_folder()

# 確認用のテーブルのスクリーンショット
get_table(driver)

# 終了
driver.quit()
