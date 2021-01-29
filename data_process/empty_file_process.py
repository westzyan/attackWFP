import os
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed

def is_empty_file_1(file_path: str):
    assert isinstance(file_path, str), f"file_path参数类型不是字符串类型: {type(file_path)}"
    assert os.path.isfile(file_path), f"file_path不是一个文件: {file_path}"
    return os.path.getsize(file_path) == 0


def is_bad_file(filepath):
    data_list = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            data_list.append(line)
    f.close()
    if len(data_list) < 200:
        print("bad file:", filepath)
    return len(data_list) < 200

# print(is_empty_file_1("/media/zyan/文档/毕业设计/code/attack_dataset/round10/tcp/68/50.csv"))



def get_cor(directory):
    split_file = directory + "split_time.txt"
    df = pd.read_csv(split_file, header=None)
    name_time = np.array(df)
    correspondence = {}
    for item in name_time:
        correspondence[str(item[0])] = float(item[1])
    print(correspondence)
    return correspondence


def search_bad_file_single(directory, label):
    label = str(label)
    empty_file_list = []
    files = os.listdir(directory + label)
    for file in files:
        full_file = directory + label + "/" + file
        if is_empty_file_1(full_file) is True:
            empty_file_list.append(str(label) + "-" + file)
        elif is_bad_file(full_file) is True:
            empty_file_list.append(str(label) + "-" + file)
    return empty_file_list


def search_empty_file(directory):
    empty_file_list = []
    # for i in range(100):
    #     full_dir = directory + "tcp/" + str(i)
    #     files = os.listdir(full_dir)
    #     for file in files:
    #         full_file = full_dir + "/" + file
    #         if is_empty_file_1(full_file) is True:
    #             empty_file_list.append(str(i) + "-" + file)
    #         elif is_bad_file(full_file is True):
    #             empty_file_list.append(str(i) + "-" + file)
    # print(empty_file_list)
    executor = ProcessPoolExecutor(max_workers=20)
    all_task = [executor.submit(search_bad_file_single, directory + "tcp/", i)for i in range(100)]
    for item in as_completed(all_task):
        data = item.result()
        empty_file_list = empty_file_list + data
    print(empty_file_list)
    return empty_file_list



def save_dict(web_dict, filepath):
    with open(filepath + "new_split_time_v1.1.txt", 'w') as f:
        for item in web_dict.keys():
            f.write(item + "," + str(web_dict[item]) + "\n")
    f.close()



if __name__ == '__main__':
    filepath = "/media/zyan/文档/毕业设计/code/attack_dataset/round8/"
    empty_files = search_empty_file(filepath)
    print(len(empty_files))
    with open(filepath + "empty.txt", 'w') as f:
        f.writelines(empty_files)
    f.close()
    web_dict = get_cor(filepath)
    for item in empty_files:
       try:
           label = item[:-4].split("-")[0]
           instance = item[:-4].split("-")[1]
           if instance == '0':
               new_instance = '99'
           else:
               new_instance = int(instance) - 1
           rm_cmd = "rm {}tcp/{}/{}.csv".format(filepath, label, instance)
           cp_cmd = "cp {}tcp/{}/{}.csv {}tcp/{}/{}.csv".format(filepath, label, new_instance, filepath, label,
                                                                instance)
           print(rm_cmd)
           print(cp_cmd)
           os.system(rm_cmd)
           os.system(cp_cmd)
           web_dict[item[:-4]] = web_dict[label + "-" + str(new_instance)]
       except Exception as e:
           print(item,"error",str(e))
    save_dict(web_dict, filepath)
