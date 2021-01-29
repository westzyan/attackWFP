import os
import time
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def cmp(a1, a2):
    return int(a1) - int(a2)


# 为split_time 中的每个时间添加对应的数据包
def add_label_to_time(filepath):
    dirs = os.listdir(filepath)
    new_dirs = []
    for dir_ in dirs:
        if not dir_.__contains__('.'):
            new_dirs.append(int(dir_))
    print(len(new_dirs))

    split = np.loadtxt(filepath + "split_time.txt")
    print(type(split))
    print(split)
    print(len(split))

    new_split = []
    new_dirs.sort()
    # new_dirs = sorted(new_dirs, key=cmp)
    for item in new_dirs:
        for i in range(100):
            new_split.append(str(i) + "-" + str(item))
    a = [new_split, split]
    a = np.array(a).T
    df = pd.DataFrame(a)
    df.to_csv(filepath + "new_split.txt", index=False, header=False)


def merge_split_time(filepath, outpath):
    df = pd.DataFrame()
    dirs = os.listdir(filepath)
    for item in dirs:
        if os.path.isdir(filepath + item):
            df_new = pd.read_csv(filepath + item + "/" + "new_split.txt", header=None)
            print(df_new)
            df_new.to_csv(outpath + "split_time.txt", mode='a', header=False, index=None)


def save_dict(web_dict, filepath):
    with open(filepath + "new_split_location.txt", 'w') as f:
        for item in web_dict.keys():
            f.write(item + "," + str(web_dict[item]) + "\n")
    f.close()


def get_true_split_single(filepath, dir, correspondence):
    ground_truth_dict = {}
    files = os.listdir(filepath + dir)
    for file in files:
        flag = False
        full_file = filepath + dir + "/" + file
        file_name = dir + "-" + file[:-4]
        start_time = correspondence[file_name]
        data_origin = []
        try:
            df = pd.read_csv(full_file, header=None, engine='python')
            data_origin = np.array(df)
            count = 0
            for item in data_origin:
                if start_time <= float(item[4]) and item[0].startswith("192."):
                    ground_truth_dict[file_name] = count
                    flag = True
                    break
                count = count + 1
        except:
            logger.error("%s文件为空", full_file)
        if flag is False:
            ground_truth_dict[file_name] = len(data_origin) - 1
            print(len(data_origin) - 1)
            logger.error("%s文件没有ground truth", full_file)
    print(ground_truth_dict)
    return ground_truth_dict


def get_true_split_multi(directory):
    split_file = directory + "new_split_time_v1.1.txt"
    df = pd.read_csv(split_file, header=None)
    name_time = np.array(df)
    correspondence = {}
    for item in name_time:
        correspondence[str(item[0])] = float(item[1])
    print(correspondence)

    full_filepath = directory + "tcp/"
    dirs = os.listdir(full_filepath)
    executor = ProcessPoolExecutor(max_workers=20)
    all_task = [executor.submit(get_true_split_single, full_filepath, dir, correspondence) for dir in dirs]
    ground_truth_dict = {}
    for future in as_completed(all_task):
        data = future.result()
        ground_truth_dict.update(data)
    executor.shutdown()
    print(ground_truth_dict)
    save_dict(ground_truth_dict, directory)

if __name__ == '__main__':
    filepath_new = "/media/zyan/文档/毕业设计/code/attack_data/第8轮收集/2_tab_7_second/"
    filepath = "/media/zyan/文档/毕业设计/code/attack_data/第8轮收集/2_tab_7_second/"
    # add_label_to_time(filepath_new)
    outpath = "/media/zyan/文档/毕业设计/code/attack_dataset/round8/"
    # merge_split_time(filepath, outpath)

    # split_file = outpath + "new_split_time_v1.1.txt"
    # df = pd.read_csv(split_file, header=None)
    # name_time = np.array(df)
    # correspondence = {}
    # for item in name_time:
    #     correspondence[str(item[0])] = float(item[1])
    # print(correspondence)
    # get_true_split_single(outpath + "tcp/", '40', correspondence)


    get_true_split_multi(outpath)
