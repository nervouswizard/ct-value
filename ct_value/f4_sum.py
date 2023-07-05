import os, sys
import pandas as pd
import numpy as np

def sum(read_path, save_path, label_column, print=print):
    # 讀檔
    for i, filename in enumerate(os.listdir(read_path)):
        if not filename.endswith('.csv'): continue
        print(i, filename)
        data = pd.read_csv(os.path.join(read_path, filename), low_memory=False)
        data = data.drop(columns=label_column)

        nparr = data.to_numpy()
        sum = np.sum(nparr, axis = 1)

        data = pd.read_csv(os.path.join(read_path, filename), low_memory=False)
        data['sum'] = sum
        data.to_csv(os.path.join(save_path, filename), index=None)