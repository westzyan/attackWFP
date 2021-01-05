# coding=utf-8
from selenium import webdriver
import time
import os
import configparser
import time
import mkdir_util
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed



executor = ProcessPoolExecutor(max_workers=3)

def test():
    print(time.time())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=socks5://localhost:1080')
    chrome_options.add_argument("enable-automation")
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
    print(time.time())
    browser1.get("https://www.google.com")
    print(time.time())




if __name__ == '__main__':
    print(time.time())
    with open("../split_time.txt", "a") as f:
        f.write(str(time.time()) + "\n")
    f.close()
    print(time.time())
