import os
import time
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_location_second(second_list, second):
    count = 0
    for item in second_list:
        if item >= second * 1.0:
            break
        count = count + 1
    return count

def get_location_second_v1(second_list, second):
    # 考虑到单页数据包秒数不一定，可能总秒数少于8秒，所以我们8秒的按照最长的来
    count = 0
    if second_list[-1] <= second * 1.0:
        return len(second_list) - 1
    for item in second_list:
        if item >= second * 1.0:
            break
        count = count + 1
    return count


def get_split_single_dir(filepath, dir):
    all_split_list = []
    full_dir = filepath + str(dir) + "/"
    print(full_dir)
    for i in range(1000):
        full_file = full_dir + str(i)
        second_list = []
        split_list = []
        with open(full_file, "r") as f1:
            for line in f1.readlines():
                line = line.strip('\n')
                # TODO single 的 \t
                second = float(line.split("\t")[0])
                second_list.append(second)
        f1.close()
        # 从2秒到8秒取位置
        for j in range(2, 9):
            split = get_location_second_v1(second_list, j)
            split_list.append(split)
        all_split_list.append(split_list)
    print(len(all_split_list))
    return dir, all_split_list


def get_true_split_multi(directory, outpath):
    executor = ProcessPoolExecutor(max_workers=40)
    all_task = [executor.submit(get_split_single_dir, directory, dir) for dir in range(95)]
    ground_truth_dict = {}
    for future in as_completed(all_task):
        dir, data = future.result()
        ground_truth_dict[dir] = data
    executor.shutdown()
    ground_truth_list = []
    for i in range(95):
        ground_truth_list = ground_truth_list + ground_truth_dict[i]
    print(len(ground_truth_list))
    np.savetxt(outpath + "special_location.txt", ground_truth_list, fmt="%d", delimiter=",")

if __name__ == '__main__':
    # for i in range(1, 8):
    #     a = time.time()
    #     print(a)
    #     input_path = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/tcp_time_direction_len/".format(i)
    #     output_path = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/".format(i)
    #     get_true_split_multi(input_path, output_path)
    #     b = time.time()
    #     print(b)
    #     print("总用时：{}秒".format(b - a))

    a = time.time()
    print(a)
    input_path = "/media/zyan/文档/毕业设计/code/attack_dataset/round13/tcp_time_direction_len/"
    output_path = "/media/zyan/文档/毕业设计/code/attack_dataset/round13/"
    get_true_split_multi(input_path, output_path)
    b = time.time()
    print(b)
    print("总用时：{}秒".format(b - a))
