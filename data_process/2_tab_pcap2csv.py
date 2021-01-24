import os
import configparser
import os
import logging
import csv
import pandas as pd
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 获取当前文件所在目录的上一级目录，即项目所在目录
root_dir = os.path.dirname(os.path.abspath('.'))
configpath = os.path.join(root_dir, "data_config.ini")
cf = configparser.ConfigParser()
cf.read(configpath)

# parse_layer = cf.get("trace_parse", "layer")
# remote_ip = cf.get("trace_parse", "remote_ip")
remote_port = cf.get("trace_parse", "remote_port")
save_filepath = cf.get("trace_parse", "save_filepath")
save_ttdl_filepath = cf.get("trace_parse", "save_ttdl_filepath")
origin_filepath = cf.get("trace_parse", "origin_filepath")
web_num_dict = {'adobe.com_amazon.com': '0', 'amazon.com_americanexpress.com': '1',
                'americanexpress.com_apple.com': '2',
                'apple.com_archive.org': '3', 'archive.org_bbc.com': '4', 'bbc.com_bet9ja.com': '5',
                'bet9ja.com_bing.com': '6',
                'bing.com_booking.com': '7', 'booking.com_breitbart.com': '8', 'breitbart.com_canva.com': '9',
                'canva.com_chaturbate.com': '10', 'chaturbate.com_chess.com': '11', 'chess.com_cnet.com': '12',
                'cnet.com_cnn.com': '13', 'cnn.com_coinmarketcap.com': '14', 'coinmarketcap.com_craigslist.org': '15',
                'craigslist.org_dailymotion.com': '16', 'dailymotion.com_dell.com': '17', 'dell.com_detik.com': '18',
                'detik.com_digikala.com': '19', 'digikala.com_discord.com': '20', 'discord.com_disneyplus.com': '21',
                'disneyplus.com_dropbox.com': '22', 'dropbox.com_duckduckgo.com': '23', 'duckduckgo.com_ebay.com': '24',
                'ebay.com_elintransigente.com': '25', 'elintransigente.com_espn.com': '26', 'espn.com_etsy.com': '27',
                'etsy.com_ettoday.net': '28', 'ettoday.net_fandom.com': '29', 'fandom.com_flipkart.com': '30',
                'flipkart.com_foxnews.com': '31', 'foxnews.com_gamepedia.com': '32', 'gamepedia.com_github.com': '33',
                'github.com_globo.com': '34', 'globo.com_godaddy.com': '35', 'godaddy.com_google.com': '36',
                'google.com_grammarly.com': '37', 'grammarly.com_hdfcbank.com': '38',
                'hdfcbank.com_healthline.com': '39',
                'healthline.com_hulu.com': '40', 'hulu.com_ilovepdf.com': '41', 'ilovepdf.com_imdb.com': '42',
                'imdb.com_imgur.com': '43', 'imgur.com_indeed.com': '44', 'indeed.com_instagram.com': '45',
                'instagram.com_linkedin.com': '46', 'linkedin.com_mediafire.com': '47',
                'mediafire.com_mercari.com': '48',
                'mercari.com_microsoft.com': '49', 'microsoft.com_msn.com': '50', 'msn.com_naver.com': '51',
                'naver.com_netflix.com': '52', 'netflix.com_newegg.com': '53', 'newegg.com_nytimes.com': '54',
                'nytimes.com_office.com': '55', 'office.com_okezone.com': '56', 'okezone.com_onlinesbi.com': '57',
                'onlinesbi.com_paypal.com': '58', 'paypal.com_pinterest.com': '59', 'pinterest.com_pixnet.net': '60',
                'pixnet.net_primevideo.com': '61', 'primevideo.com_reddit.com': '62',
                'reddit.com_researchgate.net': '63',
                'researchgate.net_roblox.com': '64', 'roblox.com_savefrom.net': '65', 'savefrom.net_setn.com': '66',
                'setn.com_sindonews.com': '67', 'sindonews.com_slack.com': '68', 'slack.com_slideshare.net': '69',
                'slideshare.net_soundcloud.com': '70', 'soundcloud.com_speedtest.net': '71',
                'speedtest.net_spotify.com': '72',
                'spotify.com_stackexchange.com': '73', 'stackexchange.com_target.com': '74',
                'target.com_telegram.org': '75',
                'telegram.org_theguardian.com': '76', 'theguardian.com_thestartmagazine.com': '77',
                'thestartmagazine.com_tokopedia.com': '78', 'tokopedia.com_tradingview.com': '79',
                'tradingview.com_trendyol.com': '80', 'trendyol.com_tribunnews.com': '81',
                'tribunnews.com_tumblr.com': '82',
                'tumblr.com_twitter.com': '83', 'twitter.com_ups.com': '84', 'ups.com_varzesh3.com': '85',
                'varzesh3.com_vk.com': '86',
                'vk.com_w3schools.com': '87', 'w3schools.com_washingtonpost.com': '88',
                'washingtonpost.com_wayfair.com': '89',
                'wayfair.com_wellsfargo.com': '90', 'wellsfargo.com_wetransfer.com': '91',
                'wetransfer.com_whatsapp.com': '92',
                'whatsapp.com_wikihow.com': '93', 'wikihow.com_wikipedia.org': '94',
                'wikipedia.org_wordpress.com': '95',
                'wordpress.com_yahoo.com': '96', 'yahoo.com_youtube.com': '97', 'youtube.com_zillow.com': '98',
                'zillow.com_adobe.com': '99', 'adobe.com_adobe.com': '100', 'amazon.com_amazon.com': '101',
                'americanexpress.com_americanexpress.com': '102',
                'apple.com_apple.com': '103', 'archive.org_archive.org': '104', 'bbc.com_bbc.com': '105',
                'bet9ja.com_bet9ja.com': '106', 'bing.com_bing.com': '107', 'booking.com_booking.com': '108',
                'breitbart.com_breitbart.com': '109', 'canva.com_canva.com': '110',
                'chaturbate.com_chaturbate.com': '111',
                'chess.com_chess.com': '112', 'cnet.com_cnet.com': '113', 'cnn.com_cnn.com': '114',
                'coinmarketcap.com_coinmarketcap.com': '115', 'craigslist.org_craigslist.org': '116',
                'dailymotion.com_dailymotion.com': '117', 'dell.com_dell.com': '118', 'detik.com_detik.com': '119',
                'digikala.com_digikala.com': '120', 'discord.com_discord.com': '121',
                'disneyplus.com_disneyplus.com': '122',
                'dropbox.com_dropbox.com': '123', 'duckduckgo.com_duckduckgo.com': '124', 'ebay.com_ebay.com': '125',
                'elintransigente.com_elintransigente.com': '126', 'espn.com_espn.com': '127',
                'etsy.com_etsy.com': '128',
                'ettoday.net_ettoday.net': '129', 'fandom.com_fandom.com': '130', 'flipkart.com_flipkart.com': '131',
                'foxnews.com_foxnews.com': '132', 'gamepedia.com_gamepedia.com': '133', 'github.com_github.com': '134',
                'globo.com_globo.com': '135', 'godaddy.com_godaddy.com': '136', 'google.com_google.com': '137',
                'grammarly.com_grammarly.com': '138', 'hdfcbank.com_hdfcbank.com': '139',
                'healthline.com_healthline.com': '140',
                'hulu.com_hulu.com': '141', 'ilovepdf.com_ilovepdf.com': '142', 'imdb.com_imdb.com': '143',
                'imgur.com_imgur.com': '144', 'indeed.com_indeed.com': '145', 'instagram.com_instagram.com': '146',
                'linkedin.com_linkedin.com': '147', 'mediafire.com_mediafire.com': '148',
                'mercari.com_mercari.com': '149',
                'microsoft.com_microsoft.com': '150', 'msn.com_msn.com': '151', 'naver.com_naver.com': '152',
                'netflix.com_netflix.com': '153', 'newegg.com_newegg.com': '154', 'nytimes.com_nytimes.com': '155',
                'office.com_office.com': '156', 'okezone.com_okezone.com': '157', 'onlinesbi.com_onlinesbi.com': '158',
                'paypal.com_paypal.com': '159', 'pinterest.com_pinterest.com': '160', 'pixnet.net_pixnet.net': '161',
                'primevideo.com_primevideo.com': '162', 'reddit.com_reddit.com': '163',
                'researchgate.net_researchgate.net': '164',
                'roblox.com_roblox.com': '165', 'savefrom.net_savefrom.net': '166', 'setn.com_setn.com': '167',
                'sindonews.com_sindonews.com': '168', 'slack.com_slack.com': '169',
                'slideshare.net_slideshare.net': '170',
                'soundcloud.com_soundcloud.com': '171', 'speedtest.net_speedtest.net': '172',
                'spotify.com_spotify.com': '173',
                'stackexchange.com_stackexchange.com': '174', 'target.com_target.com': '175',
                'telegram.org_telegram.org': '176',
                'theguardian.com_theguardian.com': '177', 'thestartmagazine.com_thestartmagazine.com': '178',
                'tokopedia.com_tokopedia.com': '179', 'tradingview.com_tradingview.com': '180',
                'trendyol.com_trendyol.com': '181',
                'tribunnews.com_tribunnews.com': '182', 'tumblr.com_tumblr.com': '183',
                'twitter.com_twitter.com': '184',
                'ups.com_ups.com': '185', 'varzesh3.com_varzesh3.com': '186', 'vk.com_vk.com': '187',
                'w3schools.com_w3schools.com': '188', 'washingtonpost.com_washingtonpost.com': '189',
                'wayfair.com_wayfair.com': '190',
                'wellsfargo.com_wellsfargo.com': '191', 'wetransfer.com_wetransfer.com': '192',
                'whatsapp.com_whatsapp.com': '193',
                'wikihow.com_wikihow.com': '194', 'wikipedia.org_wikipedia.org': '195',
                'wordpress.com_wordpress.com': '196',
                'yahoo.com_yahoo.com': '197', 'youtube.com_youtube.com': '198', 'zillow.com_zillow.com': '199'}

local_ip_start = ["10.", "192."]


def read_trace_locations():
    dict = {}
    with open("./trace_num_locations.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            tmp = line.split(",")
            dict[tmp[0]] = int(tmp[1])
    f.close()
    return dict


def save_trace_locations(dict):
    with open("./trace_num_locations.txt", "w") as f:
        for key in dict.keys():
            f.write(key + "," + str(dict.get(key)) + "\n")
    f.close()


def temp():
    filepath = "/media/zyan/文档/毕业设计/code/origin_traffic/round3/"
    # for root, dirs, files in os.walk(filepath):
    #     print(root)  # 当前目录路径
    #     print(dirs)  # 当前路径下所有子目录
    #     print(files)  # 当前路径下所有非目录子文件
    print(os.listdir(filepath))
    files = os.listdir(filepath)
    for file in files:
        new_name = file.split("_")[0] + ".pcap"
        cmd = "mv " + filepath + file + " " + filepath + new_name
        print(cmd)
        os.system(cmd)


def temp1():
    url_list = []
    with open("../aleax_top.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split("/")[-1]
            url_list.append(line)
    web_number_dict = {}
    count = 0
    for i in url_list:
        web_number_dict[i] = 0
        count += 1
    print(web_number_dict)


def temp2():
    filepath = "/media/zyan/文档/毕业设计/code/origin_traffic/round3/"
    # for root, dirs, files in os.walk(filepath):
    #     print(root)  # 当前目录路径
    #     print(dirs)  # 当前路径下所有子目录
    #     print(files)  # 当前路径下所有非目录子文件
    print(os.listdir(filepath))
    files = os.listdir(filepath)
    for file in files:
        new_name = file.split("_")[0] + ".pcap"
        cmd = "mv " + filepath + file + " " + filepath + new_name
        print(cmd)
        os.system(cmd)


def parse_trace():
    '''
    将原始pcap文件转换为csv文件，csv文件内容为源IP，源端口，目的IP，目的端口，时间戳，长度
    trace_location_dict记录每个网站下次要保存的文件的number，由于记录number，暂时单线程
    :return:
    '''
    trace_location_dict = read_trace_locations()
    filepath = origin_filepath
    dirs = os.listdir(filepath)
    list.sort(dirs)
    for dir in dirs:
        full_dir = filepath + dir
        files = os.listdir(full_dir)
        list.sort(files)
        for file in files:
            full_file = full_dir + "/" + file
            logger.info("parse file: %s", full_file)
            web_num = web_num_dict.get(file[:-5])
            trace_num = trace_location_dict.get(file[:-5])
            cmd = 'tshark  -r ' + full_file + '  -T fields -Y "tcp.port==' + remote_port + ' " -E separator=, -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport  -e frame.time_epoch -e frame.len > ' + save_filepath + str(
                web_num) + '/' + str(trace_num) + '.csv'
            os.system(cmd)
            trace_location_dict[file[:-5]] = trace_num + 1
            logger.info(cmd)
    save_trace_locations(trace_location_dict)


def parse_trace_single_dir(dir):
    filepath = origin_filepath
    full_dir = filepath + dir
    files = os.listdir(full_dir)
    for file in files:
        full_file = full_dir + "/" + file
        logger.info("parse file: %s", full_file)
        web_num = web_num_dict.get(file[:-5])
        trace_num = dir
        cmd = 'tshark  -r ' + full_file + '  -T fields -Y "tcp.port==' + remote_port + '" -E separator=, -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport  -e frame.time_epoch -e frame.len > ' + save_filepath + str(
            web_num) + '/' + str(trace_num) + '.csv'
        os.system(cmd)
        logger.info(cmd)


def parse_trace_open_world(full_dir):
    files = os.listdir(full_dir)
    count = 4931
    for file in files:
        full_file = full_dir + "/" + file
        logger.info("parse file: %s", full_file)
        cmd = 'tshark  -r ' + full_file + '  -T fields -Y "tcp.port==' + remote_port + '" -E separator=, -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport  -e frame.time_epoch -e frame.len > ' + save_filepath + str(
            count) + '.csv'
        os.system(cmd)
        count += 1
        logger.info(cmd)


def extract_trace_open_world(input_filepath, output_filepath):
    '''
    将parse_trace一个目录下的csv文件，提取对应的特征信息，包含时间【从0开始】，方向，大小
    :param output_filepath:
    :param input_filepath:
    :return:
    '''
    remote_port_list = ["60868", "60858", "60869", "12333", "60856"]
    files = os.listdir(input_filepath)
    for file in files:
        try:
            full_file = input_filepath + file
            logger.info("开始读取文件:%s", full_file)
            with open(full_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            f.close()
            standard_time = rows[0][-2]
            new_rows = []
            for row in rows:
                src_port = row[1]
                timestamp = float(row[4]) - float(standard_time)
                len = row[5]
                if src_port not in remote_port_list:
                    new_rows.append(str(timestamp) + ",+" + str(len))
                else:
                    new_rows.append(str(timestamp) + ",-" + str(len))
            full_save_file = output_filepath + file
            logger.info("开始写入文件:%s", full_save_file)
            with open(full_save_file, 'w') as f:
                for row in new_rows:
                    f.write(row + "\n")
            f.close()

            logger.info("写入文件完毕:%s", full_save_file)
        except Exception as e:
            logger.error("文件失败：%s", file)


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


def parse_trace_mul_thread():
    '''
    将原始pcap文件转换为csv文件，csv文件内容为源IP，源端口，目的IP，目的端口，时间戳，长度
    :return:
    '''
    for i in range(100):
        mkdir(save_filepath + str(i))
    filepath = origin_filepath
    dirs = os.listdir(filepath)
    executor = ProcessPoolExecutor(max_workers=10)
    for dir in dirs:
        executor.submit(parse_trace_single_dir, dir)
    executor.shutdown()


def extract_trace_files(dir):
    '''
    将parse_trace一个目录下的csv文件，提取对应的特征信息，包含时间【从0开始】，方向，大小
    :param files:
    :return:
    '''
    remote_port_list = ["60857", "60858"]
    input_filepath = save_filepath
    output_filepath = save_ttdl_filepath
    files = os.listdir(input_filepath + "/" + dir)
    for file in files:
        try:
            full_file = save_filepath + dir + "/" + file
            logger.info("开始读取文件:%s", full_file)
            with open(full_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            f.close()
            standard_time = rows[0][-2]
            new_rows = []
            for row in rows:
                src_port = row[1]
                timestamp = float(row[4]) - float(standard_time)
                len = row[5]
                if src_port not in remote_port_list:
                    new_rows.append(str(timestamp) + ",+" + str(len))
                else:
                    new_rows.append(str(timestamp) + ",-" + str(len))
            full_save_file = output_filepath + dir + "/" + file
            logger.info("开始写入文件:%s", full_save_file)
            with open(full_save_file, 'w') as f:
                for row in new_rows:
                    f.write(row + "\n")
            f.close()

            logger.info("写入文件完毕:%s", full_save_file)
        except Exception as e:
            logger.error("文件失败：%s", file)


def extract_trace():
    '''
    提取trace流
    :return:
    '''
    for i in range(100):
        mkdir(save_ttdl_filepath + str(i))
    executor = ProcessPoolExecutor(max_workers=30)
    dirs = os.listdir(save_filepath)
    logger.info("dirs: %s", dirs)
    for dir in dirs:
        executor.submit(extract_trace_files, dir)
    executor.shutdown()


def extract_feature_single_dir(dir):
    last_list = []
    input_filepath = save_ttdl_filepath
    files = os.listdir(input_filepath + "/" + dir)
    for file in files:
        last_single_list = [0] * 5000
        origin_single_list = []
        full_file = input_filepath + dir + "/" + file
        logger.info("开始读取文件:%s", full_file)
        with open(full_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        f.close()
        for row in rows:
            if row[1][0] == "+":
                origin_single_list.append(1)
            else:
                origin_single_list.append(-1)
        origin_length = 0
        if len(origin_single_list) < 5000:
            origin_length = len(origin_single_list)
        else:
            origin_length = 5000
        for i in range(origin_length):
            last_single_list[i] = origin_single_list[i]
        last_single_list.append(int(dir))
        last_list.append(last_single_list)
        logger.info("file %s, len: %s", full_file, len(last_list))
    return last_list


def extract_feature_single_dir_simulator(dir):
    last_list = []
    input_filepath = save_ttdl_filepath
    files = os.listdir(input_filepath + "/" + dir)
    for file in files:
        try:
            last_single_list = [0] * 5000
            origin_single_list = []
            full_file = input_filepath + dir + "/" + file
            # logger.info("开始读取文件:%s", full_file)
            with open(full_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            f.close()
            # random.shuffle(rows)
            for row in rows:
                if row[1][0] == "+":
                    origin_single_list.append(1)
                else:
                    origin_single_list.append(-1)
            origin_length = 0
            if len(origin_single_list) < 5000:
                origin_length = len(origin_single_list)
            else:
                origin_length = 5000
            for i in range(origin_length):
                last_single_list[i] = origin_single_list[i]
            last_single_list.append(int(dir))
            last_list.append(last_single_list)
        except:
            logger.error("file %s error", input_filepath + dir + "/" + file)
    logger.info("file %s, len: %s", input_filepath + dir, len(last_list))
    return last_list


def extract_feature():
    executor = ProcessPoolExecutor(max_workers=30)
    input_filepath = save_ttdl_filepath
    dirs = os.listdir(input_filepath)
    logger.info("dirs: %s", dirs)
    all_task = [executor.submit(extract_feature_single_dir_simulator, dir) for dir in dirs]
    last_list = []
    for future in as_completed(all_task):
        single_list = future.result()
        last_list = last_list + single_list
    print(len(last_list))
    executor.shutdown()
    data = pd.DataFrame(data=last_list)
    data.to_csv("/media/zyan/文档/毕业设计/code/attack_dataset/round2/df_tcp_10000.csv", index=False, header=False)


def extract_feature_open_world(filepath):
    dir = filepath
    logger.info("dirs: %s", dir)
    last_list = []
    files = os.listdir(dir)
    for file in files:
        try:
            last_single_list = [0] * 5000
            origin_single_list = []
            full_file = dir + file
            # logger.info("开始读取文件:%s", full_file)
            with open(full_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            f.close()
            # random.shuffle(rows)
            for row in rows:
                if row[1][0] == "+":
                    origin_single_list.append(1)
                else:
                    origin_single_list.append(-1)
            origin_length = 0
            if len(origin_single_list) < 5000:
                origin_length = len(origin_single_list)
            else:
                origin_length = 5000
            for i in range(origin_length):
                last_single_list[i] = origin_single_list[i]
            last_single_list.append(50)
            last_list.append(last_single_list)
        except:
            logger.error("file %s error", dir + file)
    logger.info("file %s, len: %s", dir, len(last_list))
    print(len(last_list))
    data = pd.DataFrame(data=last_list)
    data.to_csv("/media/zyan/文档/毕业设计/code/dataset/round10/df_OW_5000.csv", index=False, header=False)


# a = {'adobe.com': 0, 'aliexpress.com': 0, 'amazon.com': 0, 'apple.com': 0, 'baidu.com': 0, 'bing.com': 0, 'breitbart.com': 0, 'chaturbate.com': 0, 'cnn.com': 0, 'craigslist.org': 0, 'csdn.net': 0, 'dropbox.com': 0, 'ebay.com': 0, 'espn.com': 0, 'etsy.com': 0, 'foxnews.com': 0, 'hulu.com': 0, 'imdb.com': 0, 'indeed.com': 0, 'instagram.com': 0, 'jd.com': 0, 'live.com': 0, 'livejasmin.com': 0, 'microsoft.com': 0, 'naver.com': 0, 'netflix.com': 0, 'nytimes.com': 0, 'office.com': 0, 'okezone.com': 0, 'okta.com': 0, 'qq.com': 0, 'reddit.com': 0, 'salesforce.com': 0, 'sina.com.cn': 0, 'sohu.com': 0, 'stackoverflow.com': 0, 'tribunnews.com': 0, 'twitch.tv': 0, 'twitter.com': 0, 'vk.com': 0, 'walmart.com': 0, 'washingtonpost.com': 0, 'wellsfargo.com': 0, 'wikipedia.org': 0, 'www.alipay.com': 0, 'yahoo.com': 0, 'yandex.ru': 0, 'youtube.com': 0, 'zhanqi.tv': 0, 'zillow.com': 0}
# save_trace_locations(a)


def extract_trace_files_test(dir):
    '''
    将parse_trace一个目录下的csv文件，提取对应的特征信息，包含时间【从0开始】，方向，大小
    :param files:
    :return:
    '''
    input_filepath = save_filepath
    output_filepath = save_ttdl_filepath
    files = os.listdir(input_filepath + "/" + dir)
    for file in files:
        full_file = save_filepath + dir + "/" + file
        logger.info("开始读取文件:%s", full_file)
        with open(full_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        f.close()
        standard_time = rows[0][-2]
        new_rows = []
        for row in rows:
            src_ip = row[0]
            timestamp = float(row[4]) - float(standard_time)
            len = row[5]
            if src_ip.startswith(local_ip_start[0]) or src_ip.startswith(local_ip_start[1]):
                new_rows.append(str(timestamp) + ",+" + str(len))
            else:
                new_rows.append(str(timestamp) + ",-" + str(len))
        full_save_file = output_filepath + dir + "/" + file
        logger.info("开始写入文件:%s", full_save_file)
        with open(full_save_file, 'w') as f:
            for row in new_rows:
                f.write(row + "\n")
        f.close()

        logger.info("写入文件完毕:%s", full_save_file)


if __name__ == '__main__':
    # print(time.time())
    parse_trace_mul_thread()
    # print(time.time())
    # extract_trace()
    # time.sleep(5)
    # extract_feature()

    # parse_trace_open_world('/media/zyan/文档/毕业设计/code/第10轮收集/new_open_world_2/round1')
    # input = '/media/zyan/文档/毕业设计/code/dataset/round10/tcp/'
    # output = '/media/zyan/文档/毕业设计/code/dataset/round10/tcp_time_direction_len/'
    # # extract_trace_open_world(input, output)
    # extract_feature_open_world(output)
