from keras.models import load_model
import time
import argparse
import pickle
import cv2
import os
from datetime import date
import glob

# 加载測試數據
x = glob.glob('測試圖片路徑/*')[-1]
image = cv2.imread(x)
output = image.copy()
image = cv2.resize(image, (32, 32))



# scale圖像數據
image = image.astype("float") / 255.0

# 對圖像進行拉平操作
image = image.flatten()
image = image.reshape((1, image.shape[0]))

# 讀取模型和標籤
print("------讀取模型和標籤------")
model = load_model('儲存路徑/simple_nn.h5')
lb = pickle.loads(open('儲存路徑/simple_nn_lb3.pickle', "rb").read())

# 预测
preds = model.predict(image)

# 得到预测结果以及其对应的标签
i = preds.argmax(axis=1)[0]
label = lb.classes_[i]
print('辨識結果:',label)



#以時間做標記(不讓檔案覆蓋)
today = str(date.today())
a = time.localtime()
nowtime = str(time.mktime(a))
path_name = "儲存json的路徑"
try:
    os.mkdir(path_name + today)  ######### name each folder per day
except:
    print('folder exists')

with open(path_name + today + "/{}_{}.txt".format(nowtime, i), 'w') as f:
    f.write(label)


# 在圖像中把結果畫出來
text = "{}: {:.2f}%".format(label, preds[0][i] * 100)
cv2.putText(output, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
'''
'''
# 繪圖
cv2.imshow("Image", output)
cv2.waitKey(0)