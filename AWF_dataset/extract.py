import configparser
import os
import logging
import csv
import pandas as pd
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
root_dir = os.path.dirname(os.path.abspath('.'))
configpath = os.path.join(root_dir, "data_config.ini")
cf = configparser.ConfigParser()
cf.read(configpath)
remote_port = cf.get("trace_parse", "remote_port")
save_filepath = cf.get("trace_parse", "save_filepath")
save_ttdl_filepath = cf.get("trace_parse", "save_ttdl_filepath")
origin_filepath = cf.get("trace_parse", "origin_filepath")
df_filepath = cf.get("trace_parse", "save_df_filepath")

def extract_file_100(filepath, outpath):
    for i in range(95):
        for j in range(100):
            full_file = "{}{}-{}".format(filepath, i, j)
            out_file = "{}{}/{}".format(outpath, i, j)
            cmd = "cp {} {}".format(full_file, out_file)
            print(cmd)
            os.system(cmd)

def extract_file_1000(filepath, outpath):
    for i in range(95):
        for j in range(1000):
            full_file = "{}{}-{}".format(filepath, i, j)
            out_file = "{}{}/{}".format(outpath, i, j)
            cmd = "cp {} {}".format(full_file, out_file)
            print(cmd)
            os.system(cmd)


def extract_feature_single_dir_simulator(dir):
    last_list = []
    input_filepath = save_ttdl_filepath
    files = os.listdir(input_filepath + "/" + dir)
    for file in files:
        # try:
        last_single_list = [0] * 5000
        origin_single_list = []
        full_file = input_filepath + dir + "/" + file
        # logger.info("开始读取文件:%s", full_file)
        with open(full_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
        f.close()
        # random.shuffle(rows)
        for row in rows:
            if row[1][0] != "-":
                origin_single_list.append(1)
            else:
                origin_single_list.append(-1)
        origin_length = 0
        if len(origin_single_list) < 5000:
            origin_length = len(origin_single_list)
        else:
            origin_length = 5000
        # for i in range(origin_length):
        #     last_single_list[i] = origin_single_list[i]

        count = 0
        for i in range(5000 - origin_length, 5000):
            last_single_list[i] = origin_single_list[count]
            count = count + 1


        last_single_list.append(int(dir))
        last_list.append(last_single_list)
        # except Exception as e:
        # print(str(e))
        # logger.error("file %s error", input_filepath + dir + "/" + file)
    logger.info("file %s, len: %s", input_filepath + dir, len(last_list))
    return last_list


def extract_feature():
    executor = ProcessPoolExecutor(max_workers=30)
    input_filepath = save_ttdl_filepath
    dirs = os.listdir(input_filepath)
    logger.info("dirs: %s", dirs)
    all_task = [executor.submit(extract_feature_single_dir_simulator, dir) for dir in dirs]
    last_list = []
    for future in as_completed(all_task):
        single_list = future.result()
        last_list = last_list + single_list
    print(len(last_list))
    executor.shutdown()
    data = pd.DataFrame(data=last_list)
    data.to_csv(df_filepath, index=False, header=False)


def read_trace_locations():
    dict = {}
    with open("../top100.csv", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            tmp = line.split(",")
            dict[tmp[1]] = tmp[0]
    f.close()
    print(dict)
    return dict

if __name__ == '__main__':
    origin = "/media/zyan/文档/毕业设计/code/参考代码/undef_data/undefended/"
    dest = "/media/zyan/文档/毕业设计/code/attack_dataset/round15/tcp_time_direction_len/"
    # extract_file_100(origin, dest)
    extract_feature()
    # read_trace_locations()
    # extract_feature_single_dir_simulator("0")
