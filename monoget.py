# -*- coding: utf-8 -*-

"""

Created on Wed Dec 12 11:20:36 2018

@author: takano.hiroyuki

"""

import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

import csv
from collections import defaultdict

from time import sleep
import monoauth 
import monolog

class monoGet:
    home = os.getcwd()
    csv_path = home + u'\\target.csv'
    url = 'http://mnrate.com'
    no=1
    program_name = "monoget"
    user_id = ""
    

    def csvLoad(self):
        columns = defaultdict(list) # each value in each column is appended to a list
        
        with open(monoGet.csv_path) as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v) # append the value into the appropriate list
                                         # based on column name k

        target_list = columns['asincd'] 
        #df = pd.read_csv(monoGet.csv_path)
        #df = csv.reader(csv_path, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        return(target_list)
        
    def GetDriver(self):
        driver_path = self.home + u'\\chromedriver.exe'
        ##driver_path = home + u'\\chromedriver.exe'

        # Driver オブジェクトの作成
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')  ## バックグラウンド実行オプション
        options.add_extension(self.home + u'\\monozon.crx') ## Chrome Ext :: monozon
        #options.add_extension(home + u'\\monozon.crx')
        driver = webdriver.Chrome(driver_path, chrome_options = options)
        
        # 商品のURLへアクセス
        driver.get(monoGet.url)
        self._wait()
        return(driver)

    def AccessTopPage(self, driver, asin_cd, col_header):

        # 検索したいワードを入力フォームに入力する
        driver.find_element_by_name('kwd').send_keys(asin_cd)

        # 検索ボタンを実行する
        driver.find_element_by_id('_graph_search_btn').click() 

        # テーブル内容取得 
        tableElem = driver.find_element_by_class_name("table-bordered")
        trs = tableElem.find_elements(By.TAG_NAME, "tr")
                
        ## 商品名を取得する
        org_link_list = drv.find_elements_by_class_name("original_link")
        item_name = org_link_list[4].text
        
        ## 商品カテゴリを取得する
        strong = drv.find_elements_by_class_name("_strong")
        item_categoly_name = strong[0].text
        
        
        ## データ用 データフレーム を作る 出品者以降
        #val_df = pd.DataFrame(index=[], columns=(col_header))

        ## ディメンション用 データフレームを作る ASIN:商品名:商品カテゴリ
        item_list = []
        item_list = [self.no, asin_cd, item_name, item_categoly_name]

        ## 対象行 : 2行目と3行目
        for i in range(2,4):
            tds = trs[i].find_elements(By.TAG_NAME, "td")

            ## 行
            for j in range(1,5):
                val = tds[j].text
                item_list.append(val)
                #print(val)
            ## Dataframe にデータを追加
        
        self.no+=1
        ## textファイルへ出力する
        ## df.to_csv(self.home + u'\\' + asin_cd + '.csv', index=False)
        return(item_list)

    def CloseDriver(driver, self):
        driver.close()

    def _wait(self):
        sleep(1)
       

if __name__ == "__main__":
    ## 認証実施
    Autentication = monoauth.monoAuth()
    if Autentication[0] == False:
        raise Exception('Authentication faild.....')

    scr = monoGet()
    scr.user_id = Autentication[1]    
    
    asin_list = scr.csvLoad()
    drv = scr.GetDriver()
    ## monorate へアクセス
    
    #scr.htmlparse(asin_cd)
    exec_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    out_csv = (os.getcwd() + u'\\' + exec_date + '-dataset' + '.csv')    
    
    ## 出力用ファイルの作成
    f = open(out_csv, 'w', newline='')
    writer = csv.writer(f)    
    ## 行ヘッダー
    col_header = ( \
            'No', 'ASINコード', '商品名', '商品カテゴリー', \
            '新品過去1ヶ月目販売数', '新品過去2ヶ月目販売数', '新品過去3ヶ月目販売数', '新品平均月間販売数', \
            '中古過去1ヶ月目販売数', '中古過去2ヶ月目販売数', '中古過去3ヶ月目販売数', '中古平均月間販売数' \
            )
    # Create Header ------------------------------
    writer.writerow(col_header)

    ## Print Message
    str_df_length = str(len(asin_list))
    print("===============================================")
    print(" monoget : Hello!! ")
    print("===============================================")
    print("このウィンドウは閉じないでください Google Chrome が起動します")
    print(str_df_length + "件 のデータを取得します")
    
    ## monolog Insert
    monolog.monogetLogInsert(userid = scr.user_id, prgname = scr.program_name, count = str_df_length, )

    ## monoget の実行
    # Write Rows  ------------------------------
    for i in range(0, len(asin_list)):
        asin_cd = asin_list[i]
        
        print(str(i+1) + "/" + str_df_length + " ISINコード : " + str(asin_cd) )
        wk_item_list = scr.AccessTopPage(drv, asin_cd, col_header)
        writer.writerow(wk_item_list)
        scr._wait()
    
    f.close()
    print("-----------------------------------------------")
    print("complete!! check csv file !! " + str(exec_date) )
    print("Please close this prompt.")
    print("===============================================")
    print(" monoget: Bye!")
    print("===============================================")
    drv.close()

