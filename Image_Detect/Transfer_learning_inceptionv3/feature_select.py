from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.models import Sequential, Model
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def feature_extraction_InV3(train_data_dir, num_image, epochs):

    # 建立預訓練模型
    base_model = InceptionV3(input_shape=(299, 299, 3),weights='imagenet',include_top=False)
    x = GlobalAveragePooling2D()(base_model.output)
    model = Model(inputs=base_model.input, outputs=x)

    # 設定圖片生成器格式，載入圖片。
    generator = ImageDataGenerator(rescale=1. / 255).\
        flow_from_directory(train_data_dir,
        target_size = (299, 299),
        batch_size = 15,
        class_mode = "categorical",
        shuffle=False)

    # 產生圖片檔資料集
    # y_train是label，只需要手動設定類別數，並one-hot化。
    # x_train是data，需要利用預訓練模型來事先處理一次。
    train = generator.classes
    y_train = np.zeros((num_image, 6))
    y_train[np.arange(num_image), train] = 1
    X_train = model.predict(generator, verbose=1)
    return X_train, y_train

def train_last_layer(train_data_path, test_data_path, num_train_img, num_test_img, epochs):
    X_train, y_train = feature_extraction_InV3(train_data_path, num_train_img, epochs)
    X_test, y_test = feature_extraction_InV3(test_data_path, num_test_img, epochs)

    # 建立神經網絡模型做分類
    my_model = Sequential()
    my_model.add(BatchNormalization(input_shape=X_train.shape[1:]))
    my_model.add(Dense(1024, activation = "relu"))
    my_model.add(Dense(6, activation='softmax'))
    my_model.compile(optimizer="SGD", loss='categorical_crossentropy',metrics=['accuracy'])

    # 模型訓練
    history = my_model.fit(X_train, y_train, epochs=20,
                           validation_data=(X_test, y_test),
                           batch_size=10, verbose=1)

    my_model.save('incept.h5')
    return history

def plot_training(history_ft):

    # 標註模型訓練產生的權重
    acc = history_ft.history['accuracy']
    val_acc = history_ft.history['val_accuracy']
    loss  = history_ft.history['loss']
    val_loss = history_ft.history['val_loss']
    epoches = range(len(acc))

    # 繪製acc與loss圖
    plt.plot(epoches, acc, 'r', color='green', label='acc')
    plt.plot(epoches, val_acc, '--r', label='val_acc') #default color
    plt.title('Training and Validataion accuracy')
    plt.savefig('path_acc_x')
    plt.figure()
    plt.plot(epoches, loss, 'r', color='green', label='loss')
    plt.plot(epoches, val_loss, '--r', label='val_loss')
    plt.title('Training and Validataion loss')
    plt.savefig('path_loss_x')  # Save the current figure.plt.savefig('path') #Save the current figure.
    plt.show()

    # 打印每次反向傳播訓練的權重
    print('acc:', acc)
    print('val_acc:', val_acc)
    print('epoches:', epoches)
    print('loss:', loss)
    print('val_loss', val_loss)

if __name__=="__main__":

    # 設定模型與資料集參數。
    num_train_img =1200
    num_test_img =150
    epochs = 20
    train_data_path = "FinalData_250/train"
    test_data_path = "FinalData_250/valid"
    model=train_last_layer(train_data_path, test_data_path, num_train_img, num_test_img, epochs)
    plot_training(model)