from sklearn.preprocessing import label_binarize
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score,recall_score, f1_score,roc_auc_score, precision_recall_fscore_support, roc_curve, classification_report
import matplotlib.pyplot as plt
from Model_DF import DFNet
import random
from keras.utils import np_utils
from keras.optimizers import Adamax
import numpy as np
import os
import tensorflow as tf
import keras


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
keras.backend.tensorflow_backend.set_session(tf.Session(config=config))
# Load data for non-defended dataset for CW setting
def LoadDataNoDefCW():
    print("Loading defended dataset for closed-world scenario")
    # Point to the directory storing data
    # dataset_dir = '../dataset/ClosedWorld/NoDef/'
    # dataset_dir = "/media/zyan/软件/张岩备份/PPT/DeepFingerprinting/df-master/dataset/ClosedWorld/NoDef/"
    dataset_dir = "/media/zyan/文档/毕业设计/code/attack_dataset/round15/"
    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)
    data = np.loadtxt(dataset_dir + "df_tcp_9500_5000_new.csv", delimiter=",")
    print(data)
    np.random.shuffle(data)
    print(data)
    print(len(data))
    train_length = int(0.8 * len(data))
    valid_length = int(0.1 * len(data))
    test_length = len(data) - train_length - valid_length
    train = data[:train_length, :]
    valid = data[train_length: train_length + valid_length, :]
    test = data[train_length + valid_length:, :]

    X_train = train[:, :-1]
    y_train = train[:,-1]
    X_valid = valid[:, :-1]
    y_valid = valid[:,-1]
    X_test = test[:, :-1]
    y_test = test[:,-1]

    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)
    print("X: Testing data's shape : ", X_test.shape)
    print("y: Testing data's shape : ", y_test.shape)
    #
    return X_train, y_train, X_valid, y_valid, X_test, y_test


if __name__ == '__main__':
    random.seed(0)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # Use only CPU
    # os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    # os.environ["CUDA_VISIBLE_DEVICES"] = "1"

    description = "Training and evaluating DF model for closed-world scenario on non-defended dataset"

    print(description)
    # Training the DF model
    NB_EPOCH = 1  # Number of training epoch
    print("Number of Epoch: ", NB_EPOCH)
    BATCH_SIZE = 128  # Batch size
    VERBOSE = 2  # Output display mode
    LENGTH = 5000  # Packet sequence length
    OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)  # Optimizer

    NB_CLASSES = 100  # number of outputs = number of classes
    INPUT_SHAPE = (LENGTH, 1)

    # Data: shuffled and split between train and test sets
    print("Loading and preparing data for training, and evaluating the model")
    X_train, y_train, X_valid, y_valid, X_test, y_test = LoadDataNoDefCW()
    # Please refer to the dataset format in readme
    # K.set_image_dim_ordering("tf") # tf is tensorflow

    # Convert data as float32 type
    X_train = X_train.astype('float32')
    X_valid = X_valid.astype('float32')
    X_test = X_test.astype('float32')
    y_train = y_train.astype('float32')
    y_valid = y_valid.astype('float32')
    y_test = y_test.astype('float32')

    # we need a [Length x 1] x n shape as input to the DF CNN (Tensorflow)
    X_train = X_train[:, :, np.newaxis]
    X_valid = X_valid[:, :, np.newaxis]
    X_test = X_test[:, :, np.newaxis]

    print(X_train.shape[0], 'train samples')
    print(X_valid.shape[0], 'validation samples')
    print(X_test.shape[0], 'test samples')
    # Convert class vectors to categorical classes matrices
    y_train = np_utils.to_categorical(y_train, NB_CLASSES)
    y_valid = np_utils.to_categorical(y_valid, NB_CLASSES)
    y_test = np_utils.to_categorical(y_test, NB_CLASSES)

    # Building and training model
    print("Building and training DF model")
    model = DFNet.build(input_shape=INPUT_SHAPE, classes=NB_CLASSES)

    model.compile(loss="categorical_crossentropy", optimizer=OPTIMIZER,
                  metrics=["accuracy"])
    print("Model compiled")

    # Start training
    history = model.fit(X_train, y_train,
                        batch_size=BATCH_SIZE, epochs=NB_EPOCH,
                        verbose=VERBOSE, validation_data=(X_valid, y_valid))

    # model.save('my_model_undef_tcp_10000_round2.h5')

    # Start evaluating model with testing data
    score_test = model.evaluate(X_test, y_test, verbose=VERBOSE)
    print("Testing accuracy:", score_test[1])



    y_score = model.predict(X_test)
    # mean_accuracy = model.score(X_test, y_test)
    # print("mean_accuracy: ", mean_accuracy)
    print("predict label:", y_score)
    print(y_score == y_test)
    print(y_score.shape)
    y_score_pro = model.predict_proba(X_test)  # 输出概率
    print(y_score_pro)
    print(y_score_pro.shape)
    # y_score_one_hot = label_binarize(y_score, np.arange(95))  # 这个函数的输入必须是整数的标签哦
    # print(y_score_one_hot.shape)

    obj1 = confusion_matrix(y_test, y_score)  # 注意输入必须是整数型的，shape=(n_samples, )
    print('confusion_matrix\n', obj1)

    print('accuracy:{}'.format(accuracy_score(y_test, y_score)))  # 不存在average
    print('precision:{}'.format(precision_score(y_test, y_score, average='micro')))
    print('recall:{}'.format(recall_score(y_test, y_score, average='micro')))
    print('f1-score:{}'.format(f1_score(y_test, y_score, average='micro')))
    print('f1-score-for-each-class:{}'.format(precision_recall_fscore_support(y_test, y_score)))  # for macro
    # print('AUC y_pred = one-hot:{}\n'.format(roc_auc_score(y_one_hot, y_score_one_hot,average='micro')))  # 对于multi-class输入必须是proba，所以这种是错误的
    # y_one_hot = label_binarize(y_test, np.arange(95))
    # AUC值
    # auc = roc_auc_score(y_one_hot, y_score_pro, average='micro')  # 使用micro，会计算n_classes个roc曲线，再取平均
    # print("AUC y_pred = proba:", auc)
    # # 画ROC曲线
    # print("one-hot label ravelled shape:", y_one_hot.ravel().shape)
    # fpr, tpr, thresholds = roc_curve(y_one_hot.ravel(), y_score_pro.ravel())  # ravel()表示平铺开来,因为输入的shape必须是(n_samples,)
    # print("threshold： ", thresholds)
    # plt.plot(fpr, tpr, linewidth=2, label='AUC=%.3f' % auc)
    # plt.plot([0, 1], [0, 1], 'k--')  # 画一条y=x的直线，线条的颜色和类型
    # plt.axis([0, 1.0, 0, 1.0])  # 限制坐标范围
    # plt.xlabel('False Postivie Rate')
    # plt.ylabel('True Positive Rate')
    # plt.legend()
    # plt.show()
    #
    # # p-r曲线针对的是二分类，这里就不描述了
    #
    # ans = classification_report(y_test, y_score, digits=5)  # 小数点后保留5位有效数字
    # print(ans)



