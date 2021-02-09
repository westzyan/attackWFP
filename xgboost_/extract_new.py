import random
import numpy as np
import logging
import glob
import os
import sys
import subprocess
import argparse
from os import makedirs
import constants as ct
import multiprocessing as mp
import functools
from concurrent.futures import ProcessPoolExecutor, as_completed


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cmp(file1, file2):
    dir_1 = int(file1.split("/")[-2])
    file_name1 = int(file1.split("/")[-1])
    dir_2 = int(file2.split("/")[-2])
    file_name2 = int(file2.split("/")[-1])
    if dir_1 == dir_2:
        return file_name1 - file_name2
    else:
        return dir_1 - dir_2


def config_logger(args):
    # Set file
    log_file = sys.stdout
    if args.log != 'stdout':
        log_file = open(args.log, 'w')
    ch = logging.StreamHandler(log_file)

    # Set logging format
    ch.setFormatter(logging.Formatter(ct.LOG_FORMAT))
    logger.addHandler(ch)

    # Set level format
    logger.setLevel(logging.INFO)


def extract(features, x, times, directions):
    st = x - 50
    gaps = []
    for j in range(0, 99):
        gaps.append(times[st + j + 1] - times[st + j])
    features.append(float(np.mean(gaps)))
    features.append(float(np.std(gaps)))
    features.append(gaps[48])
    features.append(gaps[49])
    features.append(gaps[50])
    features.append(gaps[51])
    features.append(gaps[52])
    features.append(max(gaps))

    nextinc = 10
    for j in range(1, 20):
        if (directions[x + j] < 0):
            nextinc = j
            break
    features.append(times[x + nextinc] - times[x])
    features.append(times[x] - times[0])

    # packet rate should be lowest around a gap
    for j in range(1, 10):
        features.append(times[x + j * 2] - times[x - j * 2])

    # number of outgoing packets should be highest around a gap

    count = 0
    for j in range(0, 11):
        if (directions[x + j] > 0):
            count += 1
    features.append(count)
    count = 0
    for j in range(0, 6):
        if (directions[x + j] > 0):
            count += 1
    features.append(count)
    count = 0
    for j in range(0, 11):
        if (directions[x - j] > 0):
            count += 1
    features.append(count)
    count = 0
    for j in range(0, 6):
        if (directions[x - j] > 0):
            count += 1
    features.append(count)


def readfile(infile, times, directions):
    f = open(infile, "r")
    l = f.readlines()
    f.close()

    for x in l:
        x = x.split(",")
        times.append(float(x[0]))
        directions.append(int(x[1]))


def writefile(outfile, features):
    f = open(outfile, "w")
    for feat in features:
        f.write(str(feat) + "\n")
    f.close()


def get_truesplit(times, directions):
    # also does basic checking on whether or not the file is too bad to work
    if len(directions) < 3:
        logging.warning("This file's length is {}, abnormal".format(len(directions)))
        return None
    # for i in range(len(directions)-1):
    #     if abs(int(directions[i+1])) != abs(int(directions[i])):
    #         return i+1
    # return -1

    truesplits = []
    cnt = 2
    for i in range(1, len(directions)):
        direction = int(directions[i])
        if abs(direction) > 800:
            continue
        if direction == cnt:
            truesplits.append(i)
            cnt += 1
        # if (abs(int(directions[i])) < 888 and (   abs(int(directions[i])) != abs(int(directions[i-1])))    ):
        #     truesplits.append(i)

    # print("truesplits", truesplits)
    # f1count = 0
    # f2count = 0
    # for i in range(0, len(directions)):
    #     if (abs(directions[i]) == 1):
    #         f1count += 1
    #     if (abs(directions[i]) == 2):
    #         f2count += 1

    # if (f1count < 50 or f2count < 50):
    #     truesplit = -1

    # if (truesplit < 50):
    #     truesplit = -1

    return truesplits


def read_split_location():
    dir_ = args.t
    split_file = dir_[:-23] + "split_location.txt"
    split_list = np.loadtxt(split_file, delimiter=",")
    return split_list


def my_get_true_split(file):
    dir_ = int(file.split("/")[-2])
    file_name = int(file.split("/")[-1])
    truesplits = []
    split_list = read_split_location()
    truesplits.append(int(split_list[dir_][file_name]))
    return truesplits


def parse_arguments():
    parser = argparse.ArgumentParser(description='XGboost split algorithm.')

    parser.add_argument('t',
                        metavar='<traces path>',
                        help='Path to the directory with the traffic traces to be simulated.')
    parser.add_argument('-mode',
                        metavar='<mode>',
                        default='train',
                        help='Extract features for training set or test set.')
    parser.add_argument('--log',
                        type=str,
                        dest="log",
                        metavar='<log path>',
                        default='stdout',
                        help='path to the log file. It will print to stdout by default.')

    # Parse arguments
    args = parser.parse_args()
    config_logger(args)
    return args


def parallel(flist, testfolder, n_jobs=40):
    pool = mp.Pool(n_jobs)
    pool.map(work, zip(flist, [testfolder] * len(flist)))


def work(file):
    f = file[0]
    testfolder = file[1]
    fname = f.split('/')[-2] + "-" + f.split('/')[-1]
    logger.debug('extract feature for file {}'.format(f))
    times = []
    directions = []
    badfile = 0
    try:
        readfile(f, times, directions)
    except:
        badfile = 1
    data_dict = {'feature': [], 'location': [], 'truesplits': []}
    # truesplits = get_truesplit(times, directions)
    truesplits = my_get_true_split(f)
    data_dict['truesplits'] = truesplits

    if (badfile == 0 and truesplits != None):
        for x in range(50, len(times) - 50):
            if directions[x] > 0:
                features = []
                extract(features, x, times, directions)
                data_dict['feature'].append(features)
                data_dict['location'].append(x)
    else:
        dic = {1: 'bad', 0: 'good'}
        logger.warning('File {} is {}. True split is {}.'.format(f, dic[badfile], truesplits))

    instpath = os.path.join(testfolder, fname)
    np.save(instpath, data_dict)


def deal_train(dirpath, dir_number):
    dir_features = []
    dir_labels = []
    for filename in range(1000):
        infile = dirpath + str(dir_number) + "/" + str(filename)
        logger.debug('Processing file {}'.format(infile))
        '''1000 controls how much training data are used'''
        badfile = 0
        times = []
        directions = []
        try:
            readfile(infile, times, directions)
            logging.info('Reading file {}'.format(infile))
        except:
            badfile = 1
        # if the file is really bad don't bother
        truesplits = my_get_true_split(infile)
        logging.debug('True split is {}'.format(truesplits))

        if (badfile == 0 and truesplits != None):
            gb = [[], []]
            gb[0].extend(truesplits)
            baddies = []
            # TODO  为什么是50？？？
            for i in range(50, len(directions) - 50):
                if (0 < directions[i] < 999) and i not in truesplits:
                    baddies.append(i)
            # TODO 这里岂不是每次都是只取出来了一个？？
            if len(baddies) > 1:
                bad = np.random.choice(baddies, min(len(truesplits), len(baddies)), False)
                gb[1].extend(bad)

            np.random.shuffle(gb[0])
            np.random.shuffle(gb[1])

            for gbi in range(0, 2):
                for i in range(0, len(gb[gbi])):
                    features = []
                    x = gb[gbi][i]
                    extract(features, x, times, directions)
                    dir_features.append(features)
                    dir_labels.append(gbi)
    print(len(dir_features))
    print(len(dir_labels))
    return dir_features, dir_labels



if __name__ == '__main__':
    args = parse_arguments()
    logger.debug("Arguments: %s" % (args))
    executor = ProcessPoolExecutor(max_workers=40)
    if args.mode == 'test':
        tmp = args.t.split('/')[-3]
        testfolder = os.path.join(ct.outputdir, tmp)
        if not os.path.exists(testfolder):
            makedirs(testfolder)
        fpath = os.path.join(args.t, '*/*')
        flist = glob.glob(fpath)
        parallel(flist, testfolder)

        # for f in flist:
        #     fname = f.split('/')[-1].split(".")[0]
        #     logging.info('extract feature for file {}'.format(f))
        #     times = []
        #     directions = []
        #     badfile = 0
        #     try:
        #         readfile(f, times, directions)
        #     except:
        #         badfile = 1
        #     data_dict = {'feature':[],'location':[],'truesplits':[]}    
        #     truesplits = get_truesplit(times, directions)
        #     data_dict['truesplits'] = truesplits

        #     if (badfile == 0 and truesplits != None):
        #         for x in range(50, len(times) - 50):
        #             if directions[x] > 0:
        #                 features = []
        #                 extract(features, x, times, directions)
        #                 data_dict['feature'].append(features)
        #                 data_dict['location'].append(x)
        #     else:
        #         dic = {1:'bad', 0:'good'}
        #         logger.warning('File {} is {}. True split is {}.'.format(f,dic[badfile],truesplits))      

        #     instpath = os.path.join(testfolder, fname)         
        #     np.save(instpath, data_dict)

    elif args.mode == 'train':
        # fpath = os.path.join(args.t, '*/*')
        data_dict = {'feature': [], 'label': []}
        all_task = []
        for dir in range(95):
            task = executor.submit(deal_train, args.t, dir)
            all_task.append(task)
        for result in as_completed(all_task):
            features, labels = result.result()
            data_dict['feature'] = data_dict['feature'] + features
            data_dict['label'] = data_dict['label'] + labels
        logger.info("len feature:{}, len label:{}".format(data_dict['feature'], data_dict['label']))
        logger.debug("Training set shape:{}".format(np.array(data_dict['feature']).shape))
        print(ct.outputdir)
        print(args.t.split('/')[-3])
        outputdir = ct.outputdir + args.t.split('/')[-3]
        print(outputdir)
        np.save(outputdir, data_dict)
        logger.debug("Training set is saved to {}".format(outputdir))
    else:
        logger.error('Wrong mode:{}'.format(args.mode))
