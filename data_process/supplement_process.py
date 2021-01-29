import os


def cp_file(origin, des):
    for i in range(75, 100):
        origin_file = origin + str(i) + "/zillow.com_adobe.com.pcap"
        des_file = des + "2_tab_2_second_number_4/" + str(i) + "/zillow.com_adobe.com.pcap"
        cp_cmd = "cp {} {}".format(origin_file, des_file)
        print(cp_cmd)
        os.system(cp_cmd)


def cp_split_time(origin, des):
    split_time_list = []
    with open(origin + "split_time.txt", 'r') as f:
        for line in f.readlines():
            split_time_list.append(line)
    f.close()
    print(split_time_list)
    des_split_time_list = []
    with open(des + "2_tab_2_second_number_4/" + "split_time.txt", 'r') as f:
        for line in f.readlines():
            des_split_time_list.append(line)
    f.close()
    new_des_split_time_list = []
    for i in range(0, 25):
        new_des_split_time_list.extend(des_split_time_list[i * 199:(i + 1) * 199])
        new_des_split_time_list.append(split_time_list[i + 75])
    print(new_des_split_time_list)
    with open(des + "2_tab_2_second_number_4/" + "new_split_time.txt", 'w') as f:
        for item in new_des_split_time_list:
            f.write(item)
    f.close()



def tab_2_split(filepath):
    full_filepath = filepath + "2_tab_2_second_number_4/"
    for i in range(75, 100):
        dir = full_filepath + str(i)
        files = os.listdir(dir)
        for j in range(0, 200):
            full_file = dir + "/" + files[j]
            pcaps = files[j][:-5].split("_")
            # print(pcaps)
            if pcaps[0] == pcaps[1]:
                cmd = "mv {} /media/zyan/文档/毕业设计/code/attack_data/第3轮收集/2_tab_2_second_same_web/{}/{}".format(full_file, i, files[j])
                print(cmd)
                os.system(cmd)

def tab_2_split_time(filepath):
    full_filepath = filepath + "2_tab_2_second_number_1/"
    full_file = full_filepath + "new_split_time.txt"
    split_time_list = []
    with open(full_file, 'r') as f:
        for line in f.readlines():
            split_time_list.append(line)
    f.close()
    print(split_time_list)
    new_split_list1 = []
    new_split_list2 = []

    for i in range(len(split_time_list)):
        if i % 2 == 0:
            new_split_list1.append(split_time_list[i])
        else:
            new_split_list2.append(split_time_list[i])
    print(new_split_list1)
    print(new_split_list2)

    with open(full_filepath + "split_time1.txt", 'w') as f:
        for item in new_split_list1:
            f.write(item)
    f.close()
    with open(full_filepath + "split_time2.txt", 'w') as f:
        for item in new_split_list2:
            f.write(item)
    f.close()






if __name__ == '__main__':
    origin = "/media/zyan/文档/毕业设计/code/attack_data/第3轮收集/2_tab_2_second/2_tab_buchong/"
    des = "/media/zyan/文档/毕业设计/code/attack_data/第3轮收集/2_tab_2_second/"
    # cp_file(origin, des)
    # cp_split_time(origin, des)
    tab_2_split_time("/media/zyan/文档/毕业设计/code/attack_data/第3轮收集/2_tab_2_second/")
