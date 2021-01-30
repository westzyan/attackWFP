import os
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

def adb_shell(cmd):
    result = os.popen(cmd).read()
    print(result.split(" ")[0])
    return result


def adb_shell_dir(dir_, label):
    length_list = []
    for i in range(1000):
        cmd = "wc -l {}{}".format(dir_, i)
        print(cmd)
        result = os.popen(cmd).read()
        length_list.append(int(result.split(" ")[0]))
    print(length_list)
    return label, length_list


def wc_next(filepath, outpath, outname):
    length_list = []
    length_dict = {}
    executor = ProcessPoolExecutor(max_workers=20)
    all_task = []
    for i in range(95):
        call = executor.submit(adb_shell_dir, filepath + str(i) + "/", i)
        all_task.append(call)
    for j in as_completed(all_task):
        label, result = j.result()
        length_dict[label] = result
    print(length_dict)
    print(len(length_dict))
    for i in range(95):
        length_list.append(length_dict[i])
    np.savetxt(outpath + outname, length_list, fmt="%d", delimiter=",")


def mean(filepath):
    data = np.loadtxt(filepath, delimiter=",")
    # print(data)
    # print(np.mean(data))
    # print(np.mean(data, axis=0))
    print(np.mean(data, axis=1))


if __name__ == '__main__':
    # filepath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round1/tcp_time_direction_len/"
    # outpath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/"
    # # wc_next(filepath, outpath)
    meanpath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round2.txt"
    mean(meanpath)

    # for i in range(2, 10):
    #     filepath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/round{}/tcp_time_direction_len/".format(i)
    #     outpath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/next/"
    #     outname = "round{}.txt".format(i)
    #     wc_next(filepath, outpath, outname)