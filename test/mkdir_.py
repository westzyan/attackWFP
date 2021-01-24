import os

filepath = "/media/zyan/文档/毕业设计/code/attack_dataset/round"


for i in range(5, 12):
    cmd1 = "mkdir " + filepath + str(i)
    cmd2 = cmd1 + "/" + "tcp"
    cmd3 = cmd1 + "/" + "tcp_time_direction_len"
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)


