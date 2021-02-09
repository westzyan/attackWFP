from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, recall_score, f1_score, roc_auc_score, \
    precision_recall_fscore_support, roc_curve, classification_report
from Model_DF import DFNet
import random
from keras.utils import np_utils
from keras.optimizers import Adamax
import numpy as np
import os
import tensorflow as tf
import keras
import time
import matplotlib.pyplot as plt
import itertools


def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.　　 cm:混淆矩阵值　　 classes:分类标签　　 """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    name = time.time()
    plt.savefig(str(name) + '.jpg', dpi=300)
    plt.show()


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
keras.backend.tensorflow_backend.set_session(tf.Session(config=config))


def get_new_data(data, split_list_np, special_second):
    new_data = []
    # 找到special_second 的最大长度，当做训练长度
    max_length = np.max(split_list_np, axis=0)[special_second - 2]
    for i in range(len(data)):
        new_item  = [0] * int(max_length + 1)
        special_location = split_list_np[i][special_second - 2]
        new_item[0:special_location] = data[i][0:special_location]
        new_data.append(new_item)
    return np.array(new_data)

# Load data for non-defended dataset for CW setting
def LoadDataNoDefCW(real_second, special_second):
    print("Loading defended dataset for closed-world scenario")
    # Point to the directory storing data
    # dataset_dir = '../dataset/ClosedWorld/NoDef/'
    # dataset_dir = "/media/zyan/软件/张岩备份/PPT/DeepFingerprinting/df-master/dataset/ClosedWorld/NoDef/"
    dataset_dir = "/media/zyan/Elements/real_specified_split/second{}/".format(real_second)
    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)
    data = np.loadtxt(dataset_dir + "df_tcp_95000_10000_head_math_order.csv", delimiter=",")
    print(data[0])
    split_list_np = np.loadtxt(dataset_dir + "special_location.txt", delimiter=",")
    data = get_new_data(data, split_list_np, special_second)
    print(data[0])
    np.random.shuffle(data)
    print(data[0])
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
    for real in range(2, 9):
        for special in range(2, 9):
            random.seed(0)
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            description = "Training and evaluating DF model for closed-world scenario on non-defended dataset"
            print(description)
            # Training the DF model
            NB_EPOCH = 1  # Number of training epoch
            print("Number of Epoch: ", NB_EPOCH)
            BATCH_SIZE = 128  # Batch size
            VERBOSE = 2  # Output display mode
            OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)  # Optimizer
            NB_CLASSES = 100  # number of outputs = number of classes
            print("Loading and preparing data for training, and evaluating the model")
            X_train, y_train, X_valid, y_valid, X_test, y_test = LoadDataNoDefCW(real, special)
            LENGTH = len(X_train)  # Packet sequence length
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
            classes = [i for i in range(95)]
            plot_confusion_matrix(confmat, classes)
            with open("./real_special.txt", 'a') as f:
                f.write("real:{},special:{} acc:{}\n".format(real, special, score_test[1]))
                f.write(score)
            f.close()


if __name__ == '__main__':
    test_specified()
