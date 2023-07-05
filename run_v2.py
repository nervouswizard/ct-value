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
"""
前處理資料格式：
資料須為.csv檔案 名稱不限 有多個csv檔案也可以 但須放在同一資料夾底下
資料建議放在data/1_preprocess
csv檔案不能有行號(row), 第一行須為column name
最後一個column name須為'label'
與 label 直接相關的 column , 例如 'attack_cat' 或 'label-detail' 之類的 要在config.ini內設定
sample 部分:
所有採樣完的 csv 檔案 label 幾乎都是1:1
採樣前假設 label A與label B 數量為6:4
採樣label B 的所有資料
將 label A 以隨機採樣方式採取至 A:B 為 1:1 -> random_data
將 label A 以 column['sum'] 高到低採取至 A:B 為 1:1 -> top20_data
top20_data 的 label A 的資料再增加一些沒採取到的 feature 分布 -> HQSC_data
"""
configreader = configparser.ConfigParser()
configreader.read('config.ini', encoding='utf-8')
config = dict(configreader.items('p-value'))
del configreader
config['label_column'] = list(config['label_column'].split(' '))
config['log'] = bool(config['log'])
try:
    config['benign'] = float(config['benign'])
except:
    pass

if __name__=='__main__':
    if config['log'] == True:
        _print = print
        print = Logger.timestamped_print
        log_history(os.path.basename(__file__))
    
    # f2_score
    print('f2_score')
    read_path = config['filepath']
    save_path = os.path.join('data', '2_score')
    os.makedirs(save_path, exist_ok=True)
    score(read_path, save_path, config['label_column'], print)

    # f3_putback
    print('f3_putback')
    read_path_data = config['filepath']
    read_path_pvalue = os.path.join('data', '2_score')
    save_path = os.path.join('data', '3_DataWithPvalue')
    os.makedirs(save_path, exist_ok=True)
    putback(read_path_data, read_path_pvalue, save_path, config['label_column'], print)

    # f4_sum
    print('f4_sum')
    read_path = os.path.join('data', '3_DataWithPvalue', config['value'])
    save_path = os.path.join('data', '4_sum')
    os.makedirs(save_path, exist_ok=True)
    sum(read_path, save_path, config['label_column'], print)
    
    # f5_sample
    print('f5_sample')
    read_path_ct = os.path.join('data', '4_sum')
    read_path_ori = os.path.join(config['filepath'])
    save_path = os.path.join('data', '5_sample')
    os.makedirs(save_path, exist_ok=True)
    sample(read_path_ct, read_path_ori, save_path, config['label_column'], config['benign'], print)