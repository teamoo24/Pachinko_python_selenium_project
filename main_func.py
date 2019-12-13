from selenium.webdriver.common.by import By
# 現在のスクリーンショットを撮る
def get_screenshot(driver, path):
	page_width = driver.execute_script('return document.body.scrollWidth')
	page_height = driver.execute_script('return document.body.scrollHeight')

	driver.set_window_size(page_width, page_height)	

	driver.save_screenshot(path)

# テーブル情報を保存するメインディレクトリ指定
def make_table_folder_get_path(table_dir_name,Path):
	
	# 保存先フォルダ名
	table_dir_path = Path("table/"+table_dir_name)

	# 今日の日付のフォルダーを生成(存在してる場合スキップ)
	table_dir_path.mkdir(exist_ok=True)

	return str(table_dir_path.resolve())

def switch_driver(driver):
	driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='contents']"))

# ページ全体のソースを取得
def get_source(driver, option, nowtime, source):
	# 全体的なページのソースをdownloadページに保存
	with open('download/test_'+nowtime+option+'.html','w',encoding='utf-8') as f:
		f.write(source)

#データベースを作る
def make_database(cur):
	cur.execute('create table if not exists dedama(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,hizuke varchar(30),dai_name varchar(40),dai_no char(5),before_yesterday varchar(10),yesterday varchar(10),today varchar(10));')

# テーブル情報をデータベースに保存する前にテスト
def get_table_test(driver, table_dir, nowtime,Path, time):
	# テーブル取得
	data_table = driver.find_element_by_id("data-block")

	# テーブル目録保存
	with open(table_dir+'/'+nowtime+'.html','w',encoding='utf-8') as f:
		f.write(data_table.get_attribute('innerHTML'))

	for a in driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr[1]/td[1]/a"):
		
		# for文でテーブルごとのリンクに入る
		kishu_name = str(a.get_attribute('innerHTML'))
		
		# 保存先フォルダ名
		kishu_path = Path(table_dir+"/"+kishu_name)

		# 今日の日付のフォルダーを生成(存在してる場合スキップ)
		kishu_path.mkdir(exist_ok=True)

		#ここで該当リンクをクリック
		a.click()

		# 出玉テーブルで待機
		time.sleep(1)

		data_table = driver.find_element_by_id("container").get_attribute('innerHTML')
		get_source(driver, "_test", nowtime, data_table)

		# 本のページに戻る
		driver.back()

		time.sleep(2)



# テーブルの情報を保存
# driver : 現在のdriverの情報
# data_table : メインテーブル
def get_table(driver, table_dir, nowtime,Path, time):
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
		get_page_source(driver, str(i), nowtime, driver.page_source)
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

			except:
				print("get Error")
				get_source(driver,"error", nowtime, driver.page_source)