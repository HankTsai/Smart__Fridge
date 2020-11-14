import threading
import time
import recipe_climbing_fuction_v2 as rcf

def main(urls,store_list,name):
    for index, one_cuisine in enumerate(urls):
        recipe_dictionary = rcf.recipe_get_one(one_cuisine)
        if recipe_dictionary == None:
            print(f'{name}: index_{index} not found.')
            continue
        store_list.append(recipe_dictionary)

        if (index % 1000 == 0 or index == len(urls)-1) and index != 0:  # 每1000筆寫一次以及最後一圈把剩餘的資料寫進json
            filename = f'recipe_{name}_{index}'
            rcf.write_in_json(store_list,fileName=filename)



if __name__ == '__main__':

    start_time = time.time()

    with open('url_list.txt','r')as f:
        cuisine_urls = f.read()

    tr = []
    for i in range(4):
        t = threading.Thread(target=main,args=(cuisine_urls[i],[],f'no_{i}'))
        tr.append(t)

    for i in range(4):
        tr[i].start()
    for i in range(4):
        tr[i].join()


    end_time = time.time()
    print(f"Over, the time use: {end_time - start_time} secs")



