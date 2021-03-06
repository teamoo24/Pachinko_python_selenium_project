from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

# ページ全体のソースを取得
def get_source(driver, option, nowtime, source):
	# 全体的なページのソースをdownloadページに保存
	with open('download/test_'+nowtime+option+'.html','w',encoding='utf-8') as f:
		f.write(source)


def switch_driver(driver):
	try:
		driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='contents']"))
	except NoSuchElementException:
		get_source(driver, "_error", "error", driver.page_source)


#データベースを作る
def make_database(cur):
	# 出玉、回数、確率のテーブル作成
	cur.execute('create table if not exists dedama(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,hizuke varchar(30),dai_name varchar(40),dai_no char(5),before_yesterday varchar(10),yesterday varchar(10),today varchar(10));')
	cur.execute('create table if not exists kaisu(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,hizuke varchar(30),dai_name varchar(40),dai_no char(5),before_yesterday varchar(10),yesterday varchar(10),today varchar(10));')
	cur.execute('create table if not exists kakuritsu(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,hizuke varchar(30),dai_name varchar(40),dai_no char(5),before_yesterday varchar(10),yesterday varchar(10),today varchar(10));')


def insert_database(driver, kishu_name, nowday, time, By, cur):
	# 出玉テーブルで待機
	time.sleep(1)

	# データテーブルを受け取る
	data_table = driver.find_element_by_id("container")

	# trのリストを取得
	trs = data_table.find_elements(By.TAG_NAME, "tr")

	# 情報を保存する配列生成
	pachinko_arr = []

	for i in range(0,len(trs)):
		try:
			# tdのリストを取得
			tds = trs[i].find_elements(By.TAG_NAME, "td")
		except StaleElementReferenceException:
			print("StaleElementReferenceException")
			get_source(driver, "_StaleElementReferenceException_1", nowday, driver.page_source)
			driver.back()
			return False;

		pachinko_ind = []

		try:
			if len(tds) > 0:

				for j in range(0, len(tds)):
					pachinko_ind.append(tds[j].text)

				pachinko_arr.append(pachinko_ind)
			else :
				continue		
		except StaleElementReferenceException:
			print("StaleElementReferenceException")
			get_source(driver, "StaleElementReferenceException_2", nowday, driver.page_source)

		except WebDriverException:
			print("WebDriverException")
			print("Webドライブにエラーが発生しました。再実行します。")

	for i in range(0,len(pachinko_arr)):
		# print(pachinko_arr[i][j])
		cur.execute('INSERT INTO dedama VALUES ("", %s, %s, %s, %s, %s, %s)',(nowday,kishu_name.encode("utf-8"),pachinko_arr[i][0],pachinko_arr[i][1],pachinko_arr[i][2],pachinko_arr[i][3]))
		cur.execute('INSERT INTO kaisu VALUES ("", %s, %s, %s, %s, %s, %s)',(nowday,kishu_name.encode("utf-8"),pachinko_arr[i][0],pachinko_arr[i][4],pachinko_arr[i][5],pachinko_arr[i][6]))
		cur.execute('INSERT INTO kakuritsu VALUES ("", %s, %s, %s, %s, %s, %s)',(nowday,kishu_name.encode("utf-8"),pachinko_arr[i][0],pachinko_arr[i][7],pachinko_arr[i][8],pachinko_arr[i][9]))
		# 0 : 台番号
		# 1 : 出玉データ(一昨日)
		# 2 : 出玉データ(昨日)
		# 3 : 出玉データ(今日)
		# 4 : 回数(一昨日)
		# 5 : 回数(昨日)
		# 6 : 回数(今日)
		# 7 : 確率(一昨日)
		# 8 : 確率(昨日)
		# 9 : 確率(今日)


# テーブルの情報を保存
# driver : 現在のdriverの情報
# data_table : メインテーブル
def get_table(driver, nowtime, nowday, Path, time, cur):
	# テーブル取得
	try:
		data_table = driver.find_element_by_id("data-block")

	except NoSuchElementException:
		print("get_table error")
		get_source(driver, "_NoSuchElementException", nowtime, driver.page_source)
		
		# frameを変更
		switch_driver(driver)
		
		# ロード待ち
		time.sleep(1)

		# 修正
		try : 
			data_table = driver.find_element_by_id("data-block")
		except NoSuchElementException:
			driver.forward()
			print("処理乙2")
		print("処理おつ")

	# trのリストを取得
	trs = data_table.find_elements(By.TAG_NAME, "tr")

	for i in range(1,len(trs)):
		
		time.sleep(3)

		if(i > 1):
			switch_driver(driver)

		try :
			data_table = driver.find_element_by_id("data-block")
		
		except NoSuchElementException as e:
			print(e)
			get_source(driver, "148_NoSuchElementException", nowtime, driver.page_source)

		# trのリストを取得
		try:
			trs = data_table.find_elements(By.TAG_NAME, "tr")
			tds = trs[i].find_elements(By.TAG_NAME, "td")

		# テーブル列を超えた場合
		except IndexError as e:
			print("get table Error")
			print("列の配列にエラーが起きました。")
			get_source(driver,"_IndexError", nowtime, driver.page_source)
			
			# 本のページに戻る
			driver.back()
			time.sleep(1)

			return False

		except StaleElementReferenceException as e:
			print("get table Error")
			print("要素が見つかりません_1")
			get_source(driver,"_StaleElementReferenceException", nowtime, driver.page_source)	
			driver.forward()
			return False

		for j in range(0, len(tds)+1):

			try:
				if(j > 1):
					switch_driver(driver)
				data_table = driver.find_element_by_id("data-block")

				# trのリストを取得
				trs = data_table.find_elements(By.TAG_NAME, "tr")
				
				try:
					tds = trs[i].find_elements(By.TAG_NAME, "td")
				
				# テーブル行を超えた場合
				except IndexError as e:
					print("get table Error")
					print("行の配列にエラーが起きました。")
					get_source(driver,"IndexError", nowtime, driver.page_source)
					# 本のページに戻る
					driver.back()
					return False;

				for a in driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr["+str(i)+"]/td["+str(j)+"]/a"):
					
	    			# for文でテーブルごとのリンクに入る
					kishu_name = str(a.get_attribute('innerHTML'))
					print(kishu_name+"を作業")

					a.click()

					# データベースに挿入
					insert_database(driver, kishu_name, nowday, time, By, cur)
					
					# 本のページに戻る
					driver.back()

					time.sleep(1)

			except IndexError as e:
				print("get table Error")
				print(e)
				get_source(driver,"IndexError", nowtime, driver.page_source)
				continue

			except NoSuchElementException as e:
				print("get table Error")
				print(e)
				get_source(driver,"NoSuchElementException", nowtime, driver.page_source)