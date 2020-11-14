import json
import re
'''
step 1. 從所有食譜中擷取出食材及調味料的用量 key: ingredient, seasoning
step 2. regex分析用量詞，拆開成數量跟量詞，存成list
step 3. 將所有食材的數量跟量詞的list 的值寫入一個txt黨  -->麵粉,200,gram 
step 4. txt黨: 從裡面進行分類，做成一個大字典1號
step 5. 利用dict.items(),計算每種食材的平均用量,存成json (大字典2號)
step 6. 利用大字典2號json替換本來食譜內用量為非重量或體積單位的資訊
step 7. 寫成新的json (recipe_V6)
大字典1號{'蜜餞':[[3,'粒'],[5,gram].......], '薑':[ 3, '片'], '糯米粉': [140, 'gram']}
大字典2號(平均用量): {'蜜餞':[100,'gram], '薑':[ 3, 'gram'], '糯米粉': [140, 'gram']}
'''

# 讀取所有data
with open(r'./dataset/recipe1014_V6.json', 'r',encoding='utf-8')as f:
    #content=f.read()
    content = json.loads(f.read())

# #print(content)
# #print('所有data:',content[:5])
def aver(eachs):
    try:
        #number_item = re.match(r"(\W)*",each_item).group()  # \w 字母、數字
        #c = re.match(r"(\d)+[\W]*(\d)*",eachs).group()  # \d只取數值  \W 字母、數字  #match只找開頭
        #c = re.search(r"(\d)+[\W]*(\d)*|r'\(.*\)|\（.*\）|\《.*\》'", eachs).group()
        c = re.search(r"(\d)+[\W]*(\d)*", eachs).group()
        if "." in re.split(r"\d",c):
            return eval(c)
        elif "-" in re.split(r"\d",c) or "~" in re.split(r"\d",c) or "～" in re.split(r"\d",c):  # 20201017 修改: 新增"～"的篩選
            return eval(re.split(r"\D",c)[1])

            # return (eval(re.split(r"\D",c)[0])+eval(re.split(r"\D",c)[1]))/2  #取平均
            # round(a/b,2)
        elif "/" in re.split(r"\d",c) or "／" in re.split(r"\d",c):
            # a = Decimal(str(a)).quantize(Decimal("0.00"))
            #return eval(re.split(r"\D",c)[0])/eval(re.split(r"\D",c)[1])
            return round(eval(re.split(r"\D", c)[0]) / eval(re.split(r"\D", c)[1]),2)


        else:
            return int(c)
    except Exception as e:
        try:
            #number_tranfer = re.search('[/1234567890一ㄧ二兩三四五六七八九十\.\-\~\～\、(四分之一)(半)]+(.*)',each).group(2)
            if re.match("四分之一|4分之1|四分之1", eachs) is not None:
                return 0.25

            elif re.search("一", eachs) is not None:
            # if "一" in re.match("一", each_item).group():
                return 1
            elif re.match("二|兩", eachs) != None:
                return 2
            elif re.search("三", eachs) != None:
                return 3
            elif re.search("四", eachs) != None:
                return 4
            elif re.search("五", eachs) != None:
                return 5
            elif re.search("六", eachs) != None:
                return 6
            elif re.search("七", eachs) != None:
                return 7
            elif re.search("八", eachs) != None:
                return 8
            elif re.search("九", eachs) != None:
                return 9
            elif re.search("十", eachs) != None:
                return 10
            elif re.search("半", eachs) != None:
                return 0.5
            elif re.search("一又四分之一" ,eachs) != None:
                return 1.25
            elif re.search("1又1/2" ,eachs) != None:
                return 1.5
            elif re.search("1又1/3杯" ,eachs) != None:
                return 1.3
            elif re.search("1又1/5杯" ,eachs) != None:
                return 1.2
            else:
                return None
        except:
        #print(e)
            return "number_error"

def unit_word(eachs):
    #word = re.search('[/1234567890一ㄧ二兩三四五六七八九十\.\-\~\、\－(四分之一)(半)(ml)(g)(顆)(盒)(匙約)(種起司白醬)]+(.*)', each).group(1)
    try:

        if re.match(".*G|.*g|.*公克|.*克|.*咪咪|.*巴掌", eachs) is not None:
            return "gram"
        elif re.match(".*公斤|.*[Kk][Gg]", eachs) is not None:
            return "公斤"
        elif re.match(".*斤", eachs) is not None:
            return "斤"
        elif re.match(".*兩", eachs) is not None:  # 20201017 修改: 新增重量單位:兩
            return "兩"
        elif re.match(".*適量|.*喜好|.*依個人喜好|.*隨意|.*可省略|.*些許|.*數顆|.*數瓣", eachs) is not None:
            return "適量"
        elif re.match(".*少許|.*少少許", eachs) is not None:
            return "少許"
        elif re.match(".*數顆", eachs) is not None:
            return "數顆"
        elif re.match(".*棵|.*顆.*", eachs) is not None:
            return "顆"
        elif re.match(".*毫升|.*[cC.,]+|.*[mM][lL]", eachs) is not None:  # 20201017 修改: 把c.c整合在一個[]
            return "ml"
        elif re.match(".*[公]?升|.*[lL]", eachs) is not None:
            return "公升"
        elif re.match(".*[量米杯]+", eachs) is not None:    # 20201017 修改: 新增體積單位:米杯
            return "米杯"
        elif re.match(".*大是|.*T|.*TBS|.*tbsp|.*大匙", eachs) is not None:    # 20201017 修改: 新增pattern: 大匙
            return "大匙"
        elif re.match(".*tsp|.*t|.*[小]?匙", eachs) is not None:    # 20201017 修改: 新增pattern: 小匙
            return "小匙"
        elif re.match(".*來隻", eachs) is not None:
            return "隻"
        elif re.match(".*根.*", eachs) is not None:
            return "根"
        elif re.match(".*條", eachs) is not None:
            return "條"
        elif re.search(r"(\w)+[\W]*(\w)*", eachs).group() is not None:
            return re.search('[/12２34567890一ㄧ二兩三四五六七八九十.,-~～、－／分之半()]+(.*)', eachs).group(1)  # 20201017 修改: []內部用加escape
        elif eachs == None:     # 20201017 修改: return 改為None 非字串'None'
            pass
        else:
            return re.search('[/12２34567890一ㄧ二兩三四五六七八九十.,-~～、－／分之半()]+(.*)', eachs).group(1)
    # except Exception as e:
    #     try:
    #         if re.search("./斤", eachs) != None:
    except:
        return None

def unit_change(quantity,unit):
    if quantity != None:
        if unit == '斤':
            return quantity * 600,'gram'
        elif unit == '公斤':
            return quantity * 1000, 'gram'
        elif unit == '兩':     # 20201017 修改: 新增單位換算:兩
            return quantity * 37.8, 'gram'
        elif unit == '公升':
            return quantity * 1000, 'ml'
        elif unit == '米杯':    # 20201017 修改: 新增單位換算:米杯
            return quantity * 180, 'ml'
        else:
            return quantity,unit
    else:
        return quantity, unit

# 去除括號內容
not_brackets = r'\(.*\)|\（.*\）|\《.*\》|\，.*\|\,.*\|\（.*\|\ '

# 查看第0項 --> [['雞蛋', '2顆'], ['太白粉', '2小匙'], ...,['鰹魚粉', '1小匙']]
# ing_list1 = content[0]['ingredient']
# ing_list1 += content[0]['seasoning']
# print('ing_list:',ing_list1)

# step 1.
unit_total_list=[]
# 抓出食材、調味料
for i in content:
    ing_list = i['ingredient']
    ing_list += i['seasoning']
    #print('ing_list:',ing_list)

# step 2.
    for eachs in ing_list:
        print(eachs)   # ['鹽', '2小匙']
        name = eachs[0]
        # 1 --> 針對單位去除括號內容
        unit = re.sub(not_brackets,'',eachs[1])
        #print(unit)
        # 2 -- > 分別用量跟單位
        quantity = aver(unit)
        unit_name = unit_word(unit)
        # 3 -- > 轉換單位
        new_q,new_unit = unit_change(quantity,unit_name)

        # 單位是''或None抓出來
        # if new_unit == '' or (new_unit == None):
        #     print(i['recipe'],i['ingredient'],i['seasoning'])

        unit_list =[]
        unit_list.append(name)
        unit_list.append(new_q)
        unit_list.append(new_unit)
        unit_total_list.append(unit_list)  #unit_list=['麵粉', '360', '克']

        # print('eachs:',eachs[:5])  # ['牛奶', '160ml']
        # print('unit:',unit_list) # ['牛奶', 160, 'ml']
    #print('unit_total_list:',unit_total_list[:5])


# step 3.
# 寫入txt 這裡要改寫,只寫進list裡的值，用迴圈抓出來依序寫入-->麵粉,200,gram
fileObject = open('recipe_unit_List.txt', 'w',encoding='utf-8')
for data in unit_total_list:
    item = data[0] + ',' + str(data[1]) + ',' + str(data[2])
    # print(item)
    # print(type(item))
    fileObject.write(item+'\n')
fileObject.close()