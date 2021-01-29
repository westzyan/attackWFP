import os


def mkdir(path):
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return True
    else:
        return False


if __name__ == '__main__':
    path = "/media/zyan/文档/毕业设计/code/attack_dataset/round15/tcp_time_direction_len/"
    for i in range(95):
        mkdir(path + str(i))
