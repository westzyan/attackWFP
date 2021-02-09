from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, classification_report
from Model_DF import DFNet
import random
from keras.utils import np_utils
from keras.optimizers import Adamax
import numpy as np
import os
import tensorflow as tf
import keras
import time

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
keras.backend.tensorflow_backend.set_session(tf.Session(config=config))


def get_new_data(data, second_list, second, single_instance):
    # 按照秒数的前几秒取样，每个类别取前single_instance个样本，最大长度按照1500
    new_data = []
    max_length = 300 * (second - 1)
    for i in range(95):
        new_item = [0] * int(max_length + 1)
        # 原始的1000个样本
        label_list = data[i * 1000:(i + 1) * 1000]
        # 取前 single_instance个
        label_new_list = label_list[0:single_instance]
        for j in range(single_instance):
            all_number = i * 1000 + j
            length = int(second_list[all_number][second - 1])
            if length >= max_length:
                length = max_length
            new_item[0:length] = label_new_list[j][0:length]
            new_item[-1] = i
            new_data.append(new_item)
    print(len(new_data))
    print(len(new_data[0]))
    return np.array(new_data)


# Load data for non-defended dataset for CW setting
def LoadDataNoDefCW(second, single_instance):
    print("Loading defended dataset for closed-world scenario")
    dataset_dir = "/media/zyan/文档/毕业设计/code/attack_dataset/round13/"
    data = np.loadtxt(dataset_dir + "df_tcp_95000_5000_head_math_order.csv", delimiter=",")
    second_list = np.loadtxt(dataset_dir + "special_location.txt", delimiter=",")
    data = get_new_data(data, second_list, second, single_instance)
    np.random.shuffle(data)
    print(len(data))
    train_length = int(0.8 * len(data))
    valid_length = int(0.1 * len(data))
    test_length = len(data) - train_length - valid_length
    train = data[:train_length, :]
    valid = data[train_length: train_length + valid_length, :]
    test = data[train_length + valid_length:, :]

    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_valid = valid[:, :-1]
    y_valid = valid[:, -1]
    X_test = test[:, :-1]
    y_test = test[:, -1]

    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)
    print("X: Testing data's shape : ", X_test.shape)
    print("y: Testing data's shape : ", y_test.shape)
    #
    return X_train, y_train, X_valid, y_valid, X_test, y_test


def test_specified():
    for second in range(2, 9):
        for single_instance in range(50, 1001, 50):
            random.seed(0)
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            description = "Training and evaluating DF model for closed-world scenario on non-defended dataset"
            print(description)
            # Training the DF model
            NB_EPOCH = 20  # Number of training epoch
            print("Number of Epoch: ", NB_EPOCH)
            BATCH_SIZE = 128  # Batch size
            VERBOSE = 2  # Output display mode
            OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)  # Optimizer
            NB_CLASSES = 95  # number of outputs = number of classes
            print("Loading and preparing data for training, and evaluating the model")
            X_train, y_train, X_valid, y_valid, X_test, y_test = LoadDataNoDefCW(second, single_instance)
            LENGTH = len(X_train[0])  # Packet sequence length
            INPUT_SHAPE = (LENGTH, 1)
            X_train = X_train.astype('float32')
            X_valid = X_valid.astype('float32')
            X_test = X_test.astype('float32')
            y_train = y_train.astype('float32')
            y_valid = y_valid.astype('float32')
            y_test = y_test.astype('float32')
            X_train = X_train[:, :, np.newaxis]
            X_valid = X_valid[:, :, np.newaxis]
            X_test = X_test[:, :, np.newaxis]
            print(X_train.shape[0], 'train samples')
            print(X_valid.shape[0], 'validation samples')
            print(X_test.shape[0], 'test samples')
            y_train = np_utils.to_categorical(y_train, NB_CLASSES)
            y_valid = np_utils.to_categorical(y_valid, NB_CLASSES)
            y_test = np_utils.to_categorical(y_test, NB_CLASSES)
            print("Building and training DF model")
            model = DFNet.build(input_shape=INPUT_SHAPE, classes=NB_CLASSES)
            model.compile(loss="categorical_crossentropy", optimizer=OPTIMIZER,
                          metrics=["accuracy"])
            print("Model compiled")
            history = model.fit(X_train, y_train,
                                batch_size=BATCH_SIZE, epochs=NB_EPOCH,
                                verbose=VERBOSE, validation_data=(X_valid, y_valid))

            # model.save('my_model_undef_tcp_10000_round2.h5')
            score_test = model.evaluate(X_test, y_test, verbose=VERBOSE)
            print("Testing accuracy:", score_test[1])

            y_pre = model.predict(X_test)
            index_test = np.argmax(y_test, axis=1)
            index_pre = np.argmax(y_pre, axis=1)

            print(precision_recall_fscore_support(index_test, index_pre, average='macro'))
            # Macro-P,Macro-R,Macro-F1
            print(precision_recall_fscore_support(index_test, index_pre, average='micro'))
            # Micro-P,Micro-R,Micro-F1
            score = classification_report(index_test, index_pre)
            print(score)
            # 混淆矩阵并可视化
            confmat = confusion_matrix(y_true=index_test, y_pred=index_pre)  # 输出混淆矩阵
            print(confmat)
            with open("./increase_instance_second.txt", 'a') as f:
                f.write("second:{},all instances:{} acc:{}\n".format(second, single_instance * 95, score_test[1]))
                f.write(score)
            f.close()


if __name__ == '__main__':
    test_specified()
