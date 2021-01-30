import os
import time
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_split_single_dir(filepath, dir):
    split_list = []
    full_dir = filepath + str(dir) + "/"
    print(full_dir)
    for i in range(1000):
        full_file = full_dir + str(i)
        count = 0
        with open(full_file, "r") as f1:
            for line in f1.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                web_number = line.split(",")[-1]
                if web_number == '2':
                    break
                count = count + 1
        f1.close()
        split_list.append(count)
    return dir, split_list


def get_true_split_multi(directory, outpath):
    executor = ProcessPoolExecutor(max_workers=20)
    all_task = [executor.submit(get_split_single_dir, directory, dir) for dir in range(95)]
    ground_truth_dict = {}
    for future in as_completed(all_task):
        dir, data = future.result()
        ground_truth_dict[dir] = data
    executor.shutdown()
    ground_truth_list = []
    for i in range(95):
        ground_truth_list.append(ground_truth_dict[i])
    print(len(ground_truth_list))
    np.savetxt(outpath + "split_location.txt", ground_truth_list, fmt="%d", delimiter=",")

if __name__ == '__main__':
    # filepath_new = "/media/zyan/文档/毕业设计/code/attack_data/第8轮收集/2_tab_7_second/"
    # filepath = "/media/zyan/文档/毕业设计/code/attack_data/第8轮收集/2_tab_7_second/"
    # # add_label_to_time(filepath_new)
    # outpath = "/media/zyan/文档/毕业设计/code/attack_dataset/round8/"
    # # merge_split_time(filepath, outpath)
    #
    # # split_file = outpath + "new_split_time_v1.1.txt"
    # # df = pd.read_csv(split_file, header=None)
    # # name_time = np.array(df)
    # # correspondence = {}
    # # for item in name_time:
    # #     correspondence[str(item[0])] = float(item[1])
    # # print(correspondence)
    # # get_true_split_single(outpath + "tcp/", '40', correspondence)
    # get_true_split_multi(outpath)
    for i in range(4, 10):
        a = time.time()
        print(a)
        input_path = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/tcp_time_direction_len/".format(i)
        output_path = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/".format(i)
        get_true_split_multi(input_path, output_path)
        b = time.time()
        print(b)
        print("总用时：{}秒".format(b - a))
