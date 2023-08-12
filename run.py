"""
會將程式的輸出加上時間戳記
並同步儲存於Log資料夾中
"""
import os, sys, time

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

class Logger(object):
    def __init__(self, filename='Log/default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    @classmethod
    def timestamped_print(self, *args, **kwargs):
        _print(time.strftime("[%Y/%m/%d %X]"), *args, **kwargs)

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass

def log_history(name_s_log):
    # log
    createFolder('Log/')
    sys.stdout = Logger('Log/' + name_s_log + '.log', sys.stdout)
    sys.stderr = Logger('Log/' + name_s_log + '.err', sys.stderr)

import configparser
from ct_value.f2_score import score
from ct_value.f3_putback import putback
from ct_value.f4_sum import sum
from ct_value.f5_sample import sample
from ct_value.f6_map_testset import map_testset
from ct_value.f7_sum_testest import do_sum

configreader = configparser.ConfigParser()
configreader.read('config.ini', encoding='utf-8')
config = dict(configreader.items('p-value'))
del configreader
config['label_column'] = list(config['label_column'].split(' '))
config['log'] = bool(config['log'])

if __name__=='__main__':
    if config['log'] == True:
        _print = print
        print = Logger.timestamped_print
        log_history(os.path.basename(__file__))
    
    # f2_score
    print('f2_score')
    file_path = os.path.join('data', '1_preprocess', 'train.csv')
    save_path = os.path.join('data', '2_score')
    os.makedirs(save_path, exist_ok=True)
    score(file_path, save_path, config['label_column'], print)
    
    # f3_putback
    print('f3_putback')
    file_path_data = os.path.join('data', '1_preprocess', 'train.csv')
    read_path_pvalue = os.path.join('data', '2_score')
    save_path = os.path.join('data', '3_DataWithPvalue')
    os.makedirs(save_path, exist_ok=True)
    putback(file_path_data, read_path_pvalue, save_path, config['label_column'], print)
    
    # f4_sum
    print('f4_sum')
    read_path = os.path.join('data', '3_DataWithPvalue')
    save_path = os.path.join('data', '4_sum')
    os.makedirs(save_path, exist_ok=True)
    sum(read_path, save_path, config['label_column'], config['sum_or_count01'], print)
    
    # f5_sample
    print('f5_sample')
    file_path_ct = os.path.join('data', '4_sum', config['value'], 'train.csv')
    file_path_ori = os.path.join('data', '1_preprocess', 'train.csv')
    save_path = os.path.join('data', '5_sample')
    os.makedirs(save_path, exist_ok=True)
    sample(file_path_ct, file_path_ori, save_path, config['label_column'], config['sum_or_count01'], print)
    
    # f6_map_testset
    print('f6_map_testset')
    file_path_test = os.path.join('data', '1_preprocess', 'test.csv')
    save_path = os.path.join('data', '6_mapped_test')
    os.makedirs(save_path, exist_ok=True)
    map_testset(file_path_test, save_path, config['label_column'], print)

    # f7_sum_testset
    print('f7_sum_testset')
    read_path = os.path.join('data', '6_mapped_test')
    save_path = os.path.join('data', '7_sum_test')
    os.makedirs(save_path, exist_ok=True)
    do_sum(read_path, save_path, config['label_column'], print)