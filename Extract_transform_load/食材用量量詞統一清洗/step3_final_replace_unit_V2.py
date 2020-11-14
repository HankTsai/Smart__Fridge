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
with open('./dataset/recipe1017_V7.json', 'r',encoding='utf-8')as f:
    content = json.loads(f.read())

with open('mean_q.json', 'r',encoding='utf-8')as f:
    mean_json = json.loads(f.read())


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

# 抓出食材、調味料

for i in content:
    ing_list = i['ingredient']
    sea_list = i['seasoning']
    # print('ing_list:',ing_list)

# step 6.
    for idx,eachs in enumerate(ing_list):
        name = eachs[0]
        # 1
        unit = re.sub(not_brackets, '', eachs[1])
        # print(unit)
        # 2
        quantity = aver(unit)
        unit_name = unit_word(unit)
        # 3
        new_q, new_unit = unit_change(quantity, unit_name)

        if new_unit != 'gram' and new_unit != 'ml':
                if name in mean_json:
                    new_q = mean_json[name][0]
                    new_unit = mean_json[name][1]

        #print(new_q,new_unit)
        i['ingredient'][idx] = [name,new_q,new_unit]

    for idx, eachs in enumerate(sea_list):
        name = eachs[0]
        # 1
        unit = re.sub(not_brackets, '', eachs[1])
        # print(unit)
        # 2
        quantity = aver(unit)
        unit_name = unit_word(unit)
        # 3
        new_q, new_unit = unit_change(quantity, unit_name)

        if new_unit != 'gram' and new_unit != 'ml':
            if name in mean_json:
                new_q = mean_json[name][0]
                new_unit = mean_json[name][1]
        #print(new_q, new_unit)
        i['seasoning'][idx] = [name, new_q, new_unit]

# step 7.
# 寫成新的json
recipe_string = json.dumps(content)
with open('recipe1018_V8.json','w', encoding='utf-8') as f:
    f.write(recipe_string)

### ------------------------------------- ####
# 最後完成json_V8

# with open('recipe1018_V8.json', 'r',encoding='utf-8')as f:
#     #content=f.read()
#     content = json.loads(f.read())
# # 看全部字典
# for i in content:
#     pprint.pprint(i)
#
#     #看食材、調味料
#     ing_list = i['ingredient']
#     ing_list += i['seasoning']
#     #pprint.pprint(ing_list)