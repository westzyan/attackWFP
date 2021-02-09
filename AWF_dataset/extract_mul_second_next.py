import os
import numpy as np
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract(dir_list, output_file):
    new_data = []
    for dir_ in dir_list:
        file = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/df_tcp_95000_10000_head_math_order.csv".format(
            dir_)
        logger.info(file)
        label_count = 0
        instance_count = 0
        count = 0
        data = []
        with open(file, 'r') as f:
            for line in f.readlines():
                data.append(line.strip('\n'))
        f.close()
        for i in range(95):
            logger.info("dir:{} label:{}".format(dir_, i))
            label_list = data[i * 1000 : (i + 1) * 1000]
            new_data.extend(label_list[0:300])
    with open (output_file, 'w') as f1:
        for item in new_data:
            f1.write(item + "\n")
    f.close()


if __name__ == '__main__':
    dir_list = [1,2,3,4,5,6,7,8]
    output_file = '/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/df_2345678*95*300_second.txt'
    extract(dir_list, output_file)
