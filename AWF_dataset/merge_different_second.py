import os
import logging
import csv
import pandas as pd
import numpy as np
import random
import time
import mkdir_util
from concurrent.futures import ProcessPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

filepath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round7/tcp_time_direction_len/"


def single(website_label):
    for i in range(2, 10):
        cmd = "cp  /media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/tcp_time_direction_len/{}/* /media/zyan/文档/毕业设计/code/AWF_attack_dataset/different_second/第1轮single/{}/{}/".format(
            i, website_label, website_label, i - 2)
        logger.info(cmd)
        os.system(cmd)

def extract_feature_single_dir_order(filepath, dir, length):
    last_list = []
    input_filepath = filepath
    for file in range(1000):
        file = str(file)
        # try:
        last_single_list = [0] * length
        origin_single_list = []
        full_file = input_filepath + dir + "/" + file
        # logger.info("开始读取文件:%s", full_file)
        with open(full_file, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            rows = list(reader)
        f.close()
        for row in rows:
            if row[1][0] != "-":
                origin_single_list.append(1)
            else:
                origin_single_list.append(-1)
        origin_length = 0
        if len(origin_single_list) < length:
            origin_length = len(origin_single_list)
        else:
            origin_length = length
        for i in range(origin_length):
            last_single_list[i] = origin_single_list[i]
        # count = 0
        # for i in range(5000 - origin_length, 5000):
        #     last_single_list[i] = origin_single_list[count]
        #     count = count + 1
        last_single_list.append(int(dir))
        last_list.append(last_single_list)
    logger.info("file %s, len: %s", input_filepath + dir, len(last_list))
    return dir, last_list


def extract_feature(input_path, output_path):
    last_dict = {}
    executor = ProcessPoolExecutor(max_workers=8)
    input_filepath = input_path
    dirs = os.listdir(input_filepath)
    logger.info("dirs: %s", dirs)
    all_task = [executor.submit(extract_feature_single_dir_order, input_path, dir, 10000) for dir in dirs]
    last_list = []
    for future in as_completed(all_task):
        dir, single_list = future.result()
        last_dict[dir] = single_list
    executor.shutdown()
    for i in range(7):
        last_list = last_list + last_dict[str(i)]
    print(len(last_list))
    data = pd.DataFrame(data=last_list)
    data.to_csv(output_path + "df_7000_10000.csv", index=False, header=False)
    logger.info("over")



if __name__ == '__main__':
    # filepath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/different_second/第1轮single/"
    # for i in range(5):
    #     for j in range(95):
    #         mkdir_util.mkdir(filepath + str(i) + "/" + str(j))
    # single(5)
    for i in range(5):
        filepath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/different_second/第1轮single/{}/".format(i)
        outpath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/different_second/第1轮single/web_{}".format(i)
        extract_feature(filepath, outpath)