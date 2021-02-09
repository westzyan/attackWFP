import numpy as np
import os

# for i in range(1, 10):
#     file = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/split_location.txt".format(i)
#     data = np.loadtxt(file, delimiter=",", dtype='int')
#     # print(np.mean(data, axis=1))
#     print(np.median(data))

# file = '/media/zyan/文档/毕业设计/code/参考代码/Rimmer2018DLWF/dataset/tor_100w2500tr/labels.npy'
# data = np.load(file, allow_pickle=True)
#
# print(data.shape)
# print(data)

import pickle
file=open("/media/zyan/文档/毕业设计/code/参考代码/tik_tok_data/processed_time_features/Undefended/X_tr.pkl","rb")
data=pickle.load(file)
print(data)
print(len(data))
print(len(data[0]))
file.close()