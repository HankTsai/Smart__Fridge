import matplotlib
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers.core import Dense
from keras.optimizers import SGD
from keras import initializers
from keras import regularizers
import utils_paths  # 主要用于圖象路徑處理操作，具體代碼參考附錄
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os


#需先執行附錄檔案才可執行此檔案


print("------開始讀取數據------")
data = []
labels = []


# 拿到圖像數據路徑，方便後續讀取
imagePaths = sorted(list(utils_paths.list_images('圖庫路徑')))
random.seed(42)
random.shuffle(imagePaths)


# 讀取數據
for imagePath in imagePaths:
    # 讀取圖像數據，由於使用神經網路，需要给拉平成一维
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (32, 32)).flatten()
    data.append(image)

    # 讀取標籤
    label = imagePath.split(os.path.sep)[-2]
    labels.append(label)

# 對圖像數據做scale操作
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# 切分數據集
(trainX, testX, trainY, testY) = train_test_split(data,
                                                  labels, test_size=0.25, random_state=42)

# 轉換標籤為one-hot encoding格式
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# 構造網路模型結構：本次為3072-128-64-3
model = Sequential()
# kernel_regularizer=regularizers.l2(0.01) L2正则化项
# initializers.TruncatedNormal 初始化参数方法，截断高斯分布
model.add(Dense(128, input_shape=(3072,), activation="relu",
                kernel_initializer=initializers.TruncatedNormal(mean=0.0, stddev=0.05, seed=None),
                kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.5))
model.add(
    Dense(64, activation="relu", kernel_initializer=initializers.TruncatedNormal(mean=0.0, stddev=0.05, seed=None),
          kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.5))
model.add(Dense(len(lb.classes_), activation="softmax",
                kernel_initializer=initializers.TruncatedNormal(mean=0.0, stddev=0.05, seed=None),
                kernel_regularizer=regularizers.l2(0.01)))

# 初始化参数
INIT_LR = 0.001
EPOCHS = 2000

# 模型編譯
print("------准备训练网络------")
opt = SGD(lr=INIT_LR)
model.compile(loss="categorical_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# 擬合模型
H = model.fit(trainX, trainY, validation_data=(testX, testY),
              epochs=EPOCHS, batch_size=32)

# 測試網路模型
print("------正在评估模型------")
predictions = model.predict(testX, batch_size=32)
print(classification_report(testY.argmax(axis=1),
                            predictions.argmax(axis=1), target_names=lb.classes_))

# 繪製結果曲線
#tensorflow高於2.0版本使用accuarcy,低於2.0使用acc，此版本使用1.14.0

N = np.arange(0, EPOCHS)
plt.style.use("ggplot")
plt.figure()
plt.plot(N[1500:], H.history["acc"][1500:], label="train_acc")
plt.plot(N[1500:], H.history["val_acc"][1500:], label="val_acc")
plt.title("Training and Validation Accuracy (Simple NN)")
plt.xlabel("Epoch #")
plt.ylabel("Accuracy")
plt.legend()
plt.savefig('儲存路徑/simple_nn_plot_acc10.png')

plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
plt.title("Training and Validation Loss (Simple NN)")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend()
plt.savefig('儲存路徑/simple_nn_plot_loss.png')

# 保存模型到本地
print("------正在保存模型------")
model.save('儲存路徑/simple_nn.h5')
f = open('儲存路徑/simple_nn_lb.pickle', "wb")  # 保存标签数据
f.write(pickle.dumps(lb))
f.close()


'''
參考網址:https://reurl.cc/R1Q6n9
'''