import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from collect_trace.mkdir_util import mkdir
import matplotlib.pyplot as plt
import matplotlib
import random

def merge_single(file1, file2, label, instance, gap_second, outpath):
    f1 = np.loadtxt(file1)
    tab1 = [1] * len(f1)
    f1 = np.column_stack((f1, tab1))
    f2 = np.loadtxt(file2)
    tab2 = [2] * len(f2)
    f2 = np.column_stack((f2, tab2))
    for i in range(len(f2)):
        f2[i][0] = f2[i][0] + gap_second
    data = np.concatenate((f1, f2), axis=0)
    data = data[np.argsort(data[:, 0])]
    out_file = "{}{}/{}".format(outpath, label, instance)
    print(out_file)
    np.savetxt(out_file, data, fmt="%f,%d,%d", delimiter=",")



def merge_AWF_next(gap_second, outpath):
    filepath = "/media/zyan/文档/毕业设计/code/attack_dataset/round13/tcp_time_direction_len/"
    for i in range(95):
        mkdir("{}{}".format(outpath, i))
    executor = ProcessPoolExecutor(max_workers=30)
    for i in range(95):
        for j in range(1000):
            file1 = filepath + str(i) + "/" + str(j)
            file2 = filepath + str((i + 1) % 95) + "/" + str(j)
            executor.submit(merge_single, file1, file2, i, j, gap_second, outpath)
    executor.shutdown()

def merge():
    for i in range(3, 11):
        outpath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/random/round{}/tcp_time_direction_len/".format(i - 1)
        merge_AWF_random(i, outpath)


def merge_AWF_random(gap_second, outpath):
    filepath = "/media/zyan/文档/毕业设计/code/attack_dataset/round13/tcp_time_direction_len/"
    for i in range(95):
        mkdir("{}{}".format(outpath, i))
    executor = ProcessPoolExecutor(max_workers=20)
    for i in range(95):
        for j in range(100):
            random_num1 = random.randint(0, 1000)
            random_num2 = random.randint(0, 95)
            random_num3 = random.randint(0, 1000)
            file1 = filepath + str(i) + "/" + str(random_num1)
            file2 = filepath + str(random_num2) + "/" + str(random_num3)
            executor.submit(merge_single, file1, file2, i, j, gap_second, outpath)
    executor.shutdown()



def merge_MY():
    print(666)


def compare_instances(filepath):
    # files = os.listdir(filepath)
    single_directions_list = []
    for i in range(100):
        full_file = filepath + str(i) + ".csv"
        single_str = ''
        with open(full_file, "r") as f:
            print(full_file)
            for line in f.readlines():
                line = line.strip('\n')
                if line.split(',')[1][0] == '+':
                    single_str = single_str + '+'
                else:
                    single_str = single_str + '-'
            single_directions_list.append(single_str)
        f.close()
    print(single_directions_list)

    # with open("/media/zyan/文档/毕业设计/code/attack_dataset/round2/edition_distance/1.txt", 'w') as f:
    #     for i in range(len(single_directions_list)):
    #         for j in range(len(single_directions_list)):
    #             distance = edit_distance(single_directions_list[i], single_directions_list[j])
    #             print("{}-{} edition distance:{}".format(i, j, distance))
    #             f.write("{}-{} edition distance:{}".format(i, j, distance))
    # f.close()
    edit_list = []
    executor = ProcessPoolExecutor(max_workers=40)
    all_task = []
    for i in range(len(single_directions_list)):
        for j in range(len(single_directions_list)):
            result = executor.submit(edit_distance_single, single_directions_list[i], single_directions_list[j], i, j)
            all_task.append(result)
    for item in as_completed(all_task):
        single_result = item.result()
        edit_list.append(single_result)
    with open("/media/zyan/文档/毕业设计/code/attack_dataset/round2/edition_distance/1.txt", 'w') as f:
        for item in edit_list:
            f.write(item + "\n")
    f.close()


def edit_distance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            delta = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    return dp[len1][len2]


def edit_distance_single(word1, word2, str1, str2):
    len1 = len(word1)
    len2 = len(word2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            delta = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    print("{}-{}:{}".format(str1, str2, dp[len1][len2]))
    return "{}-{}:{}".format(str1, str2, dp[len1][len2])


def CUMUL(filepath, flag):
    CUMUL_all_list = []
    for i in range(100):
        full_file = filepath + str(i) + ".csv"
        single_str = ''
        CUMUL_single_list = []
        count = 0
        with open(full_file, "r") as f:
            print(full_file)
            for line in f.readlines():
                line = line.strip('\n')
                if flag:
                    count = count + abs(int(line.split(',')[1][1:]))
                else:
                    count = count + int(line.split(',')[1][1:])
                CUMUL_single_list.append(count)
        f.close()
        # print(CUMUL_single_list)
        # plt_CUMUL(CUMUL_single_list)
        CUMUL_all_list.append(CUMUL_single_list)
    return CUMUL_all_list


def save_CUMUL(filepath):
    for i in range(100):
        full_dir = filepath + str(i) + "/"
        cumul_list = CUMUL(full_dir, False)
        np.save("/media/zyan/文档/毕业设计/code/attack_dataset/round2/cumul/" + str(i) + ".npy", cumul_list)


def plt_CUMUL(data1, data2, str1, str2):
    print(data1)
    print(data2)
    # # 设置matplotlib正常显示中文和负号
    # matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    zhfont = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/myfonts/msyh.ttf')
    # plt.bar(range(len(data)), data,color='yellow')
    plt.style.use('ggplot')
    plt.plot(data1, linewidth=2.0, linestyle='--')
    plt.plot(data2, linewidth=2.0, linestyle='-')
    # 显示横轴标签
    plt.xlabel("个数", fontproperties=zhfont)
    # 显示纵轴标签
    plt.ylabel("累积量", fontproperties=zhfont)
    # 显示图标题
    plt.title(str1 + " " + str2 + "CUMUL", fontproperties=zhfont)
    plt.show()




if __name__ == '__main__':
    # str1 = 'abababababbbbbaaabab'
    # str2 = 'abab'
    # print(edit_distance(str1, str2))
    # filepath1 = "/media/zyan/文档/毕业设计/code/attack_dataset/round4/tcp_time_direction_len/"
    # filepath2 = "/media/zyan/文档/毕业设计/code/attack_dataset/round4/tcp_time_direction_len/18/"
    # # compare_instances(filepath)
    #
    # # CUMUL_list1 = CUMUL(filepath1, False)
    # # print(len(CUMUL_list1))
    # # print(CUMUL_list1[3])
    # #
    # # CUMUL_list2 = CUMUL(filepath2, False)
    # # print(len(CUMUL_list2))
    # # print(CUMUL_list2[31])
    # # print()
    #
    # # plt_CUMUL(CUMUL_list)
    #
    # filepath = "/media/zyan/文档/毕业设计/code/attack_dataset/round2/cumul/"
    # save_CUMUL(filepath=filepath1)
    # # label1 = random.randint(0, 100)
    # # label2 = random.randint(0, 100)
    # # instance1 = random.randint(0, 100)
    # # instance2 = random.randint(0, 100)
    # # a = np.load(filepath + "{}.npy".format(label1), allow_pickle=True)[instance1]
    # # b = np.load(filepath + "{}.npy".format(label2), allow_pickle=True)[instance2]
    # #
    # # plt_CUMUL(a, b, "{}-{}".format(label1, instance1), "{}-{}".format(label2, instance2))
    #
    # # print(plt.style.available)
    file1 = "/media/zyan/文档/毕业设计/code/参考代码/undef_data/0-0"
    file2 = "/media/zyan/文档/毕业设计/code/参考代码/undef_data/1-1"
    outpath = "/media/zyan/文档/毕业设计/code/AWF_attack_dataset/random/round1/tcp_time_direction_len/"
    # merge_single(file1, file2, 0, 1, 2, outpath)

    # merge_AWF_next(2, outpath)
    merge()
    # merge_AWF_random(2, outpath)