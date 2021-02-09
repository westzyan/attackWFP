import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#这里导入你自己的数据
#......
#......
#x_axix，train_pn_dis这些都是长度相同的list()

#开始画图
sub_axix = filter(lambda x:x%200 == 0, x_axix)
plt.title('Result Analysis')
plt.plot(x_axix, train_acys, color='green', label='training accuracy')
plt.plot(sub_axix, test_acys, color='red', label='testing accuracy')
plt.plot(x_axix, train_pn_dis,  color='skyblue', label='PN distance')
plt.plot(x_axix, thresholds, color='blue', label='threshold')
plt.legend() # 显示图例

plt.xlabel('iteration times')
plt.ylabel('rate')
plt.show()
#python 一个折线图绘制多个曲线

def plt_CUMUL(CUMUL_list, data2):
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    # 随机生成（10000,）服从正态分布的数据
    # data = np.random.randn(10000)
    data = CUMUL_list
    """
    绘制直方图
    data:必选参数，绘图数据
    bins:直方图的长条形数目，可选项，默认为10
    normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
    facecolor:长条形的颜色
    edgecolor:长条形边框的颜色
    alpha:透明度
    """
    # plt.bar(range(len(data)), data,color='yellow')
    plt.plot(data, color='red', linewidth=2.0)
    plt.plot(data2, color='blue', linewidth=2.0)
    # plt.hist(data, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
    # plt.hist(data, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
    # 显示横轴标签
    plt.xlabel("区间")
    # 显示纵轴标签
    plt.ylabel("频数/频率")
    # 显示图标题
    plt.title("频数/频率分布直方图")
    plt.show()

# for item in CUMUL_list:
#     print(len(item))
#     print(item)
#     plt_CUMUL(item)

import numpy as np
import os
import glob

def cmp(file1, file2):
    dir_1 = int(file1.split("/")[-2])
    file_name1 = int(file1.split("/")[-1])
    dir_2 = int(file2.split("/")[-2])
    file_name2 = int(file2.split("/")[-1])
    if dir_1 == dir_2:
        return file_name1 - file_name2
    else:
        return dir_1 - dir_2
import functools
import time
import pandas as pd
# if __name__ == '__main__':
    # plt_CUMUL(b, c)

    # b = 3
    # a = 0 if b ==1 else 2
    # print(a)
    # fpath = os.path.join("/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round1/tcp_time_direction_len/", '*/*')
    # flist = glob.glob(fpath)
    # print(flist)3
    # 2
    #
    # flist = sorted(flist, key=functools.cmp_to_key(cmp))
    # print(flist)
    # print(time.time())
    # a = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round1/df_tcp_95000_10000_head_math_order.csv"
    # # print(a[:-23])
    # # dic = np.load("./xgboost_/features/round5.npy", allow_pickle=True).item()
    # # features = dic['feature']
    # # labels = dic['label']
    # # print(len(features))
    # # print(len(labels))
    # # print(features[0:2])
    # b = pd.read_csv(a, header=None)
    # print(b)
    # c = b.values
    # print(c.shape)
    # print(time.time())


    # label = np.random.randint(0,95, size=(95,1))
    # print(label)