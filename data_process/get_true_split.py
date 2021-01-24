import os
import time
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv


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
            # df.append(df_new)
            # print(df)
            df_new.to_csv(outpath + "split_time.txt", mode='a', header=False, index=None)


def get_true_split_single(filepath, dir, correspondence):
    ground_truth_dict = {}
    files = os.listdir(filepath + dir)
    for file in files:
        full_file = filepath + dir + "/" + file
        file_name = dir + "-" + file[:-4]
        start_time = correspondence[file_name]
        df = pd.read_csv(full_file, header=None)
        data_origin = np.array(df)
        count = 0
        for item in data_origin:
            if start_time >= float(item[4]) and item[0].startswith("192."):
                ground_truth_dict[file_name] = count
                break
            count = count + 1
    print(ground_truth_dict)
    return ground_truth_dict


def get_true_split_multi(direction):
    split_file = direction + "split_time.txt"
    df = pd.read_csv(split_file, header=None)
    name_time = np.array(df)
    correspondence = {}
    for item in name_time:
        correspondence[str(item[0])] = float(item[1])
    print(correspondence)

    full_filepath = direction + "tcp/"
    dirs = os.listdir(full_filepath)
    executor = ProcessPoolExecutor(max_workers=10)

    # all_task = [executor.submit(get_true_split_single, full_filepath, dir, correspondence) for dir in dirs]
    ground_truth_dict = {}
    # for future in as_completed(all_task):
    #     data = future.result
    #     ground_truth_dict.update(data)
    # executor.shutdown()
    print(ground_truth_dict)


if __name__ == '__main__':
    filepath_new = "/media/zyan/文档/毕业设计/code/attack_data/第8轮收集/2_tab_7_second/2_tab_7_second_number_4/"
    filepath = "/media/zyan/文档/毕业设计/code/attack_data/第8轮收集/2_tab_7_second/"
    add_label_to_time(filepath_new)
    outpath = "/media/zyan/文档/毕业设计/code/attack_dataset/round8/"
    # merge_split_time(filepath, outpath)

    # split_file = outpath + "split_time.txt"
    # df = pd.read_csv(split_file, header=None)
    # name_time = np.array(df)
    # correspondence = {}
    # for item in name_time:
    #     correspondence[str(item[0])] = float(item[1])
    # print(correspondence)
    # get_true_split_single(outpath + "tcp/", '0', correspondence)
