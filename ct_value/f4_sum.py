import os, sys
import pandas as pd
import numpy as np

def sum(read_path, save_path, label_column, sum_or_count01, print=print):
    # 讀檔
    for i, filename in enumerate(os.listdir(read_path)):
        if not filename.endswith('.csv'): continue
        print(i, filename)
        data = pd.read_csv(os.path.join(read_path, filename), low_memory=False)
        data = data.drop(columns=label_column)
        num_columns = data.shape[1]
        nparr = data.to_numpy()
        data = pd.read_csv(os.path.join(read_path, filename), low_memory=False)
        if sum_or_count01 == 'sum':
            #avg與sum擇一使用，效果相同
            #avg = np.mean(nparr, axis=1)
            #data['avg'] = avg
            print('execute sum')
            sum = np.sum(nparr, axis = 1)
            data['sum'] = sum
        elif sum_or_count01 == 'count01':
            print('execute count01')
            count_gt_eq_0_1 = np.sum(nparr >= 0.1, axis=1)/num_columns
            data['count_gt_0_1'] = count_gt_eq_0_1
        else:
            print('something wrong.please check config.ini :sum_or_count01')
            return
        #save
        print('saving ' + filename)
        data.to_csv(os.path.join(save_path, filename), index=None)
        print('done')