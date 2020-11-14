import requests
from bs4 import BeautifulSoup
import time
import json
import pprint
import threading
import os
import queue

path = "Json_recipefiles"
if not os.path.isdir(path):
    os.mkdir(path)

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

main_page = 'https://icook.tw/categories?ref=icook-footer'

def get_catagories_url(main_page):
    catagories_list=[]
    res = requests.get(url=main_page, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    catagories = soup.select('li[class="categories-all-child"]') #算出有N類食品(106類)
    for catagories_number in range(len(catagories)):  # N類食品
        catagories_url = "https://icook.tw"+ soup.select('a[class="categories-all-child-link"]')[catagories_number]['href']
        catagories_list.append(catagories_url)
    return catagories_list

def get_cuisine_url(catagories_urls):
    cuisine_url_list = [] #每類別的所有網址
    list1, list2, list3, list4 = [],[],[],[]
    for each_catagory_url in catagories_urls:
        print(f'now is {each_catagory_url}')
        page = 1
        # for p in range(1):
        for p in range(1,1500):#每類N頁
            each_cuisine_url = each_catagory_url + '?page=%s' % (page)
            # print(each_cuisine_url)
            each_cuisine_res = requests.get(url=each_cuisine_url, headers=headers)
            catagories_soup = BeautifulSoup(each_cuisine_res.text, 'html.parser')
            page_length = catagories_soup.select('span[class="browse-recipe-name"]')
            # print(page_length)
            if page_length == []:  # 若此頁抓不到任何資料，則直接結束迴圈
                break
            # for i in range(3):
            for i in range(len(page_length)):  #每一頁細項
                cuisine_url = "https://icook.tw/" + catagories_soup.select('a[class="browse-recipe-link"]')[i]['href']
                print(cuisine_url)
                if (cuisine_url in list1) or (cuisine_url in list2) or (cuisine_url in list3) or (cuisine_url in list4):   #####################20200901
                    continue
                if p % 4 == 0:  ########################20200831###############
                    list1.append(cuisine_url)
                elif p % 4 == 1:
                    list2.append(cuisine_url)
                elif p % 4 == 2:
                    list3.append(cuisine_url)
                else:
                    list4.append(cuisine_url)
            page+=1
            print(f'page {page}')
    cuisine_url_list.append(list1)  ########################20200831###############
    cuisine_url_list.append(list2)
    cuisine_url_list.append(list3)
    cuisine_url_list.append(list4)
    return(cuisine_url_list)

def recipe_get_one(cuisine_url):
    res_cuisine = requests.get(url=cuisine_url, headers=headers)
    cuisine_soup = BeautifulSoup(res_cuisine.text, 'html.parser')

    # 食譜名稱****************
    try:
        recipe = cuisine_soup.select('h1[id="recipe-name"]')[0].text.strip()  #########################修改資訊#############
    except IndexError:
        return None

    # 讚數
    try:
        like_num = cuisine_soup.select('span[class="stat-content"]')[0].text
    except:
        like_num = '0'
    like_num = like_num.strip('說讚')

    # tag清單製作
    tag_list = []
    tag_partial = cuisine_soup.select('li[class="recipe-related-keyword-item"]')
    # print(tag)
    tag_len = (len(tag_partial))
    # print(tag_partial)
    for i in range(tag_len):
        # print(cuisine_soup.select('li[class="recipe-related-keyword-item"]')[i])
        tag = cuisine_soup.select('li[class="recipe-related-keyword-item"]')[i].select('a')[0].text
        tag_list.append(tag)
    # print(tag_list)

    # 主要圖片
    main_pic = cuisine_soup.select('div[class="recipe-details"]')[0].select('a')[0]['href']
    # print(main_pic)

    # 份量
    try:
        quantity = cuisine_soup.select('div[class="servings"]>span')[0].text
    except:
        quantity = 0  #########################修改資訊###########################
    # print(quantity)

    # 時間
    try:
        cook_time_num = cuisine_soup.select('div[class="info-content"]')[1].select('span')[0].text
        cook_time_unit = cuisine_soup.select('div[class="info-content"]')[1].select('span')[1].text
        cook_time = cook_time_num + cook_time_unit
    except:
        cook_time = 'unknown'  #########################修改資訊##########################
    # print(cook_time)

    # 材料清單製作
    ingredients_list = []
    ingredients = cuisine_soup.select('div[class="ingredient"]')
    for index, value in enumerate(ingredients):
        ingredients_n = cuisine_soup.select('div[class="ingredient"]')[index].select('a[class="ingredient-search"]')[
            0].text
        ingredients_unit = cuisine_soup.select('div[class="ingredient"]')[index].select('div[class="ingredient-unit"]')[
            0].text
        ingredients_list.append([ingredients_n, ingredients_unit])
        # print(ingredients_n)
        # print(ingredients_unit)
    # print(ingredients_list)

    # 步驟字典製作
    step = {}
    step_list = []
    step_pics_list = []
    step_all = cuisine_soup.select('li[class="step"]')
    # print(step_all)
    for index, value in enumerate(step_all):
        step_num = cuisine_soup.select('li[class="step"]')[index].select('big')[0].text
        step_content = cuisine_soup.select('li[class="step"]')[index].select('div[class="step-instruction-content"]')[
            0].text
        step_list.append('步驟' + step_num + '.' + step_content)
        # print(step_num)
        # print(step_content)

        try:
            step_pics = cuisine_soup.select('li[class="step"]')[index].select('a')[0]['href']
            step_pics_list.append('圖片' + step_num + ' ' + step_pics)
        except Exception as e:
            print(f'{index}: {e}')
            step_pics = ''
            step_pics_list.append(step_pics)
    # print(step_list)
    # print(step_pics_list)
    step['content'] = step_list
    step['stepUrl'] = step_pics_list
    # print(step)

    # 初始化dictionary
    recipe_dic = {}  ####################修改資訊#############################
    recipe_dic['recipe'] = recipe
    recipe_dic['tag'] = tag_list
    recipe_dic['url'] = cuisine_url
    recipe_dic['like'] = like_num
    recipe_dic['time'] = cook_time
    recipe_dic['image'] = main_pic
    recipe_dic['quantity'] = quantity
    recipe_dic['ingredients'] = ingredients_list
    recipe_dic['step'] = step
    pprint.pprint(recipe_dic)

    return(recipe_dic)

def write_in_json(fileList,fileName):
    with open(fileName,'w') as f:
        f.write(json.dumps(fileList))

def main(urls,store_list,name):
    for index, one_cuisine in enumerate(urls):
        recipe_dictionary = recipe_get_one(one_cuisine)
        if recipe_dictionary == None:
            print(f'{name}: index_{index} not found.')
            continue
        store_list.append(recipe_dictionary)

        if (index % 1000 == 0 or index == len(urls)-1) and index != 0:  # 每1000筆寫一次以及最後一圈把剩餘的資料寫進json
            filename = f'recipe_{name}_{index}'
            write_in_json(store_list,fileName=filename)



if __name__ == '__main__':
    start_time = time.time()

    catagories_urls = get_catagories_url(main_page)
    print(catagories_urls)
    print(len(catagories_urls))

    cc = [[] for _ in range(4)]
    sp = 1
    for cu in catagories_urls:
        if sp % 4 == 0:
            cc[0].append(cu)
        elif sp % 4 == 1:
            cc[1].append(cu)
        elif sp % 4 == 2:
            cc[2].append(cu)
        elif sp % 4 == 3:
            cc[3].append(cu)
        sp += 1
    print(cc)
    print(len(cc[0]))
    print(len(cc[1]))
    print(len(cc[2]))
    print(len(cc[3]))


    # 建立Queue 儲存thread的function return值
    que = queue.Queue()

    print('Start multithread......')
    tr = []
    for i in range(4):
        t = threading.Thread(target=lambda q, arg1: q.put(get_cuisine_url(arg1)),args=(que,cc[i]))
        tr.append(t)
    for i in range(4):
        tr[i].start()
    for i in range(4):
        tr[i].join()


    print('Multithread completed.')
    total_recipe_url = []
    for i in range(4):
        total_recipe_url += que.get()

    with open('url_list.txt','w')as f:
        for url in total_recipe_url:
            f.writelines(url + ',')

    end_time = time.time()
    print(f"Over, the time use: {end_time - start_time} secs")