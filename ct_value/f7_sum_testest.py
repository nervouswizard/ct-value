import os
import numpy as np
import pandas as pd

def do_sum(read_path, save_path, label_column, print=print):
    for i, file in enumerate(os.listdir(read_path)):
        if  file.endswith('_test.csv'): 
            print(i, '.Loading data : ' + file)
            filename = os.path.join(read_path , file)
            test = pd.read_csv(filename, low_memory=False)
            
            test['sum'] = test.drop(columns=label_column, inplace=False).sum(axis=1)
            
            test.to_csv(os.path.join(save_path, file), index=None)