url_list = []
with open("./top120.csv", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        url_list.append(line.split(",")[-1])
f.close()
print(url_list)


url_list = list(set(url_list))
print(len(url_list))
url_list.sort()
count = 0
with open("./top100.csv", "w") as f:
   for item in url_list:
       f.write("{},{}\n".format(count, item))
       count += 1
f.close()