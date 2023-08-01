import os
import numpy as np
import pandas as pd


def do_sum():
    read_path = os.path.join('data', '6_mapped_test')
    save_path = os.path.join('data', '6_mapped_test', 'sum')
    os.makedirs(save_path, exist_ok=True)
    for i, file in enumerate(os.listdir(read_path)):
        if  file.endswith('_test.csv'): 
            print(i, '.Loading data : ' + file)
            filename = os.path.join('data', '6_mapped_test' , file)
            test = pd.read_csv(filename, low_memory=False)
            
            print('--add sum start')
            
            test['sum'] = test.drop(columns='label', inplace=False).sum(axis=1)
            print('--add sum done')
            
            print('saving...')
            test.to_csv(os.path.join(save_path, file), index=None)
            print('saved ' + file)
            del file
do_sum()