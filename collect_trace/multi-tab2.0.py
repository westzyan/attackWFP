# coding=utf-8
from selenium import webdriver
import time
import os
import configparser
import time
import mkdir_util
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
# logging.basicConfig(filename='两标签页.log', level=logging.DEBUG, format=LOG_FORMAT)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=socks5://localhost:9150')
chrome_options.add_argument("enable-automation")
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("service_args=[’–ignore-ssl-errors=true’, ‘–ssl-protocol=TLSv1’]")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser1 = webdriver.Chrome(chrome_options=chrome_options)
browser1.set_page_load_timeout(40)  # 设置超时时间，
browser1.set_script_timeout(40)  # 这两种设置都进行才有效

browser2 = webdriver.Chrome(chrome_options=chrome_options)
browser2.set_page_load_timeout(40)  # 设置超时时间，
browser2.set_script_timeout(40)  # 这两种设置都进行才有效

root_dir = os.path.dirname(os.path.abspath('.'))  # 获取当前文件所在目录的上一级目录，即项目所在目录E:\Crawler
configpath = os.path.join(root_dir, "config.ini")
cf = configparser.ConfigParser()
cf.read(configpath)  # 读取配置文件

path = cf.get("collect", "origin_path")
start = int(cf.get("collect", "round_start"))
end = int(cf.get("collect", "round_end"))
eth0 = cf.get("collect", "eth0")
interval_time = int(cf.get("collect", "interval_time"))


def browser_tab(number, url):
    if number == 1:
        try:
            browser1.get("https://www." + url)
        except Exception as e:
            print("browser1 exception: " + str(e))
    else:
        logging.info(time.time())
        with open("../split_time.txt", "a") as f:
            f.write(str(time.time()) + "\n")
        f.close()
        try:
            browser2.get("https://www." + url)
        except Exception as e:
            print("browser2 exception: " + str(e))
    return 0


if __name__ == '__main__':
    url_list = []
    with open("../top100.csv", "r") as f1:
        for line in f1.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            url_list.append(line.split(",")[-1])
    f1.close()
    print(url_list)
    error_list = []
    for i in range(start, end):
        mkdir_util.mkdir(path + str(i))
    executor = ProcessPoolExecutor(max_workers=3)
    for index in range(start, end):
        logging.info("开始第%s轮次捕获", str(index))
        for url_index in range(len(url_list)):
            for next_tab_index in range(10):
                try:
                    logging.info("开始:%s_%s", url_list[url_index], url_list[(url_index + next_tab_index) % 100])
                    cmd1 = "tcpdump -i {} -w {}{}/{}_{}.pcap &".format(eth0, path, index,
                                                                       url_list[url_index].split("/")[-1],
                                                                       url_list[url_index + next_tab_index % 100].split(
                                                                           "/")[-1])
                    cmd2 = "ps -ef | grep 'tcpdump' | grep -v grep | awk '{print $2}' | xargs kill -9"
                    os.system(cmd1)
                    futures = []
                    futures.append(executor.submit(browser_tab, 1, url_list[url_index]))
                    time.sleep(interval_time)
                    futures.append(executor.submit(browser_tab, 2, url_list[(url_index + next_tab_index) % 100]))
                    for result in as_completed(futures):
                        data = result.result()
                    os.system(cmd2)
                    logging.info("结束:%s_%s", url_list[url_index], url_list[(url_index + next_tab_index) % 100])
                    time.sleep(1)
                except Exception as e:
                    print(url_list[url_index], url_list[(url_index + next_tab_index) % 100], "error", str(e))
                    logging.error("round:%s, error:%s_%s,%s", index, url_list[url_index],
                                  url_list[(url_index + next_tab_index) % 100], str(e))
                    with open("../multi_tab_2_error.txt", "a") as f2:
                        f2.write(str(index) + "," + url_list[url_index] + "_" + url_list[
                            (url_index + next_tab_index) % 100] + "\n")
                    f2.close()
                time.sleep(1)
        time.sleep(1)
