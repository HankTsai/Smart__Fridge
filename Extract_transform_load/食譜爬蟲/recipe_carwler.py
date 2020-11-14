

import json
import time
import random
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs


''' ======== 基礎函數打包 ======= '''

# 建構主頁連結與頭鏢
def request_data(header, url):
    headers = header
    home_url = url
    return headers, home_url

# 用xpath取得解析過的樹結構list
def xpath_request(url, headers):
    try:
        res = ss.get(url=url, headers=headers)
        page = etree.HTML(res.text)
        return page
    except Exception as e:
        return e

# 用bs取得解析過得樹結構html，可使用字典方式取值。
def bs4_request(url, headers):
    try:
        res = ss.get(url=url, headers=headers)
        page = bs(res.text, "html.parser")
        return page
    except Exception as e:
        return e


''' ======== 主要擷取與儲存函數 ======== '''

def create_recipi_class(home_url, headers, recipe_class):
    # 主頁進入全分類
    all_page = bs4_request(home_url, headers)
    all_graph = all_page.select('a.footer-sitemap-link')
    all_url = home_url + all_graph[-6]['href']

    # 擷取除了VIP的所有食譜分類成字典
    cla_page = bs4_request(all_url, headers)
    cla_graph = cla_page.select('a.categories-all-child-link')
    for i in cla_graph:
        recipe_class[i['name']] = home_url+i['href']


def create_recipe_link(home_url, headers, **recipe_class):
    for cla_name, cla_url in recipe_class.items():
        recipe_link = {}        #將每個類別儲存成一個字典
        page_url = cla_url      # 讓類別的網址 = 每類第一頁的網址
        next_page_exist = True  # 確認還有下一頁可以翻

        while next_page_exist:
            # 解析出當前頁面的每個食譜標籤。
            cla_sub_page = bs4_request(page_url, headers)
            cla_sub_graph = cla_sub_page.select('a.browse-recipe-link')

            # 將每個食譜標籤中的名稱與連結存成字典。
            for item in cla_sub_graph:
                recipe_link[item['aria-label']] = home_url + item['href']
            time.sleep(random.randint(0,3))

            # 抓取下一頁按鈕換頁，若無下一頁則換下一個類別。
            next_page_butt = cla_sub_page.select('a[aria-label="下一頁"]')
            if next_page_butt: page_url = home_url + next_page_butt[0]['href']
            else: next_page_exist = False

        # 將每個類別存成一個檔案。
        if '/' in cla_name: cla_name = cla_name.replace('/', '')
        js = json.dumps(recipe_link, ensure_ascii=False)
        with open(f'./recipe_class/{cla_name}.json', 'w', encoding='utf8') as file:
            file.write(js)
            print(len(js), js)
            print(f'Finish {cla_name} file stored.')

def download_recipe():



def main():
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/84.0.4147.135 Safari/537.36'}
    url = "https://icook.tw"
    headers, home_url = request_data(header, url)
    create_recipi_class(url, headers, recipe_class)
    create_recipe_link(url, headers, **recipe_class)

if __name__ == '__main__':
    ss = requests.session()
    recipe_class = {}
    main()





