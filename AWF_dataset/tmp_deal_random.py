import os

def deal_single(filepath):
    for i in range(100):
        file  = filepath + str(i)
        if not os.path.exists(file):
            next_file = str((i + 1) % 100)
            cmd = "cp {} {}".format(filepath + next_file, file)
            print(cmd)
            os.system(cmd)


if __name__ == '__main__':
    for round in range(1, 10):
        path = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/random/round{}/tcp_time_direction_len/".format(round)
        for dir_ in range(95):
            deal_single(path + str(dir_) + "/")