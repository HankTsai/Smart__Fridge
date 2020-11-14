import json
import pprint
import re
# # 讀取txt -->  content_list == txt word
with open(r'./recipe_unit_List.txt','r',encoding='utf-8') as f:
    # f=f.read() #str
    #content_list = f.readlines()
    read_list = f.readlines()
    # 針對list裡的元素（str)去掉換行符號
    content_list=[' '.join([i.strip() for i in content.strip().split('\n')]) for content in read_list]
    #content_list = [x.strip() for x in list1]

    #print(type(content_list)) #list裡面包str=='雞蛋,2,顆'
    #pprint.pprint(content_list) # ['雞蛋,2,顆', '太白粉,2,小匙', '水,50,ml,...']
    # print(content_list[0],type(content_list[0]))  # 取第0項 --> '雞蛋,2,顆' 是一個字串str
    #print(content_list[0].split(',')) #用逗號分割成3個元素--> ['雞蛋', '2', '顆'] 為list

# 將整數零頭做四捨五入
def good_number(mean_w):  # mean_w= round(total_w / count_w)
    mean_w_str = str(mean_w)  #'126'  #'46'  #'3'
    try:
        mean_w_int = int(mean_w_str[-1]) #6 #6  #3

        try:
            mean2_w_int = int(mean_w_str[-2]) #2 #4 #None


            try:  # '46'pass
                mean3_w_int = int(mean_w_str[-3]) #1 #None #None
            except:
                pass

            if mean_w_int >= 5:
               mean2_w_int += 1  #2-->3
               mean_w_int = 0    #6 -->0
            elif mean_w_int< 5:
                 mean_w_int = 0
            new_mean_w_str=str(mean_w_int)   # 3 -->'3'
            new2_mean_w_str=str(mean2_w_int)  # 0 -->'0'
            try:
                new3_mean_w_str=str(mean3_w_int)
                return int(new3_mean_w_str+new2_mean_w_str + new_mean_w_str)  # 126-->130
            except:
                return int(new2_mean_w_str + new_mean_w_str)  # 46 -->50
        except:
            return mean_w # 3 -->3
    except:
        pass

# step 4.
big_dict= {}
# 用i跑很多list裡的str(字串)， 先計算list長度==len(content_list)==for i in range(695)
for i in range(len(content_list)):
    # 用split還原list ['雞蛋', '2', '顆']
    split_item = content_list[i].split(',') #i為跑全部，逗號分割成3個元素--> ['雞蛋', '2', '顆'] 為list
    #print(split_item)

    # 為食材名稱建立[] -->  再放進[用量,'單位'] --> '名稱':[[ 用量,'單位'],[ 用量,'單位']]
    if split_item[0] not in big_dict:
        big_dict[split_item[0]] = []
    # 外迴圈--> append用量、單位在同一個食材名稱（相同名稱可能會重複，不同用量單位）
    try:
        big_dict[split_item[0]].append([split_item[1],split_item[2]]) # {'麵':[[None, 'None'],[200, 'gram']],'羊肉': [[400, 'gram'],[....]]}
    except:
        pass

#result== 每種食材所有的用量單位-->'黑豆': [['120', 'gram']],'龍眼': [['None', '適量'], ['20', 'gram']]}
#pprint.pprint(big_dict)


# step 5.　算出平均用量
ing_table = {}

# i==key-->食材名稱
# j==value --> [['1', '根'],['1', '根']....]
for i,j in big_dict.items():
    # print(f'now, processing item is {i}')

    # w-重量(gram) v-體積(ml)
    total_w,total_v = 0,0
    count_w,count_v = 0,0
    # create dict: 計算出現 gram、ml次數
    unit_ck = {'gram':0,'ml':0}
    for each in j:
        if each[0] is not "None":  # 用量-->數值
            if each[1] == 'gram':# 單位== gram
                try: # 用量有可能是None，try非數值，就pass
                    total_w += int(each[0])  #str轉int
                    count_w += 1
                    unit_ck['gram'] += 1
                except:
                    pass
            elif each[1] == 'ml':
                try:
                    total_v += int(each[0])
                    count_v += 1
                    unit_ck['ml'] += 1
                except:
                    pass

    try:
        mean_w = round(total_w / count_w)
        #print('w_舊平均:',mean_w)
        new_mean_w = good_number(mean_w)
        #print('w_新平均',new_mean_w)
    except ZeroDivisionError:
        mean_w = 0

    try:
        mean_v = round(total_v / count_v)
        #print('v_舊平均:',mean_v)
        new_mean_v = good_number(mean_v)
        #print('v_新平均:',new_mean_v)
    except ZeroDivisionError:
        mean_v = 0


    # ing_table[i] = mean_q

    # 針對單位處理，只抓用量有值的gram、ml食材資訊，並抓出對應的單位gram、ml
    if (unit_ck['gram'] == 0) and (unit_ck['ml'] == 0):
        # ing_table[i] = [0,None]
        pass
    elif unit_ck['gram'] >= unit_ck['ml']:
        ing_table[i] = [new_mean_w, 'gram']
    elif unit_ck['gram'] < unit_ck['ml']:
        ing_table[i] = [new_mean_v, 'ml']

#pprint.pprint(ing_table)   # dict==每種食材的平均用量-->{'龍蝦': [260, 'gram'],'龍鬚菜': [240, 'gram']}

# 存成json
recipe_string = json.dumps(ing_table)
with open('mean_q.json','w', encoding='utf-8') as f:
    f.write(recipe_string)
