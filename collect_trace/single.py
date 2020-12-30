# coding=utf-8
from selenium import webdriver
import time
import os
import configparser
import time
import mkdir_util
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=socks5://localhost:9150')
chrome_options.add_argument("enable-automation")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("service_args=[’–ignore-ssl-errors=true’, ‘–ssl-protocol=TLSv1’]")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_page_load_timeout(40)  # 设置超时时间，
browser.set_script_timeout(40)  # 这两种设置都进行才有效

root_dir = os.path.dirname(os.path.abspath('.'))  # 获取当前文件所在目录的上一级目录，即项目所在目录E:\Crawler
configpath = os.path.join(root_dir, "config.ini")
cf = configparser.ConfigParser()
cf.read(configpath)  # 读取配置文件

path = cf.get("collect", "origin_path")
start = int(cf.get("collect", "round_start"))
end = int(cf.get("collect", "round_end"))
eth0 = cf.get("collect", "eth0")

if __name__ == '__main__':
    url_list = []
    with open("../top100.csv", "r") as f1:
        for line in f1.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            url_list.append(line.split(",")[-1])
    f1.close()
    print(url_list)
    url_list = url_list[:120]
    error_list = []
    for i in range(start, end):
        mkdir_util.mkdir(path + str(i))
    for index in range(start, end):
        logging.info("开始第%s轮次捕获", str(index))
        for url in url_list:
            try:
                logging.info("开始:%s", url)
                cmd1 = "tcpdump -i {} -w {}{}/{}.pcap &".format(eth0, path, index, url.split("/")[-1])
                cmd2 = "ps -ef | grep 'tcpdump' | grep -v grep | awk '{print $2}' | xargs kill -9"
                os.system(cmd1)
                a = browser.get("https://www." + url)
                os.system(cmd2)
                time.sleep(2)
            except Exception as e:
                print(url, "error", str(e))
                logging.error("round:%s, error:%s,%s", index, url, str(e))
                with open("../error.txt", "a") as f2:
                    f2.write(str(index) + "," + str(url) + "\n")
                f2.close()
            time.sleep(2)
        time.sleep(2)