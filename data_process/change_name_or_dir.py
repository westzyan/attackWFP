

import os
# url_list = []

# files = os.listdir(filepath)
# print(files)
# for file in files:
#     cmd = "mv " + filepath + "/" + file + " " + filepath + "/" + file[:-7] + ".pcap"
#     print(cmd)
#     os.system(cmd)

for i in range(100):
    filepath = "/media/zyan/文档/毕业设计/code/attack_dataset/round2/tcp/"
    filepath = filepath + str(i) + "/"
    print(filepath)
    files = os.listdir(filepath)
    print(files)
    for file in files:
        new_file = str(int(file[:-4]) - 100) + ".csv"
        cmd = "mv " + filepath + file + " " + filepath + new_file
        print(cmd)
        os.system(cmd)
