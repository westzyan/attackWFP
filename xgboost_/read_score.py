import numpy as np
import os


file = "/media/zyan/文档/毕业设计/code/attackWFP/xgboost_/scores/round5/94-999-score.npy"

data = np.load(file, allow_pickle=True)
print(data)