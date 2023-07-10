from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def score(read_path, save_path, _benign, label_column, print=print):
    # 讀檔
    for i, filename in enumerate(os.listdir(read_path)):
        if not filename.endswith('.csv'): continue
        print(i, filename)
        data = pd.read_csv(os.path.join(read_path, filename))
        column_list = data.columns.to_list()

        filename = filename.replace('.csv', '/')
        os.makedirs(os.path.join(save_path, '1_statistic', '1_raw_Counter', filename), exist_ok=True)
        os.makedirs(os.path.join(save_path, '1_statistic', '2_map_table', filename), exist_ok=True)
        os.makedirs(os.path.join(save_path, '2_weight', filename), exist_ok=True)

        # 對每個feature計算各個特徵值出現的機率
        for c, col in enumerate(column_list):
            if col in label_column: continue

            print(str(c) + ' ' + col)

            b = Counter()  # b = benign
            m = Counter()  # m = malicious
            # calculate the probability

            filename = filename.replace('/', '.csv')
            data = pd.read_csv(os.path.join(read_path, filename), usecols=[col, 'label'], low_memory=False)
            filename = filename.replace('.csv', '/')

            # 將不同的label拆分為不同的資料集
            benign = data[data['label'] == _benign]
            malicious = data[data['label'] != _benign]

            # 某特徵c在label為benign/malicious出現的次數
            b += Counter(benign[column_list[c]])
            m += Counter(malicious[column_list[c]])

            bc_df = pd.DataFrame.from_dict(b, orient='index').reset_index()
            mc_df = pd.DataFrame.from_dict(m, orient='index').reset_index()
            
            #計算權重(加權ct值)
            bm_raw_counter = b + m
            weight = np.log10(np.array([value for value in bm_raw_counter.values()]))
            bm_df = pd.DataFrame.from_dict(bm_raw_counter, orient='index').reset_index()
            bm_df.insert(loc = 2, column='weight', value=weight)

            # raw counter save(出現次數)
            bc_df.to_csv(os.path.join(save_path, '1_statistic', '1_raw_Counter', filename, 
            'b_'+str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'count'])
            mc_df.to_csv(os.path.join(save_path, '1_statistic', '1_raw_Counter', filename, 
            'm_'+str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'count'])
            
            # weight save
            bm_df.to_csv(os.path.join(save_path, '2_weight', filename, 
            str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'count', 'weight'])

            for val, freq in b.items():
                b[val] = b[val] / bm_raw_counter[val]
            for val, freq in m.items():
                m[val] = m[val] / bm_raw_counter[val]

            b_pvalue_df = pd.DataFrame.from_dict(b, orient='index').reset_index()
            m_pvalue_df = pd.DataFrame.from_dict(m, orient='index').reset_index()

            # 儲存map table
            b_pvalue_df.to_csv(os.path.join(save_path, '1_statistic', '2_map_table', filename,
            'b_'+str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'pvalue'])
            m_pvalue_df.to_csv(os.path.join(save_path, '1_statistic', '2_map_table', filename,
            'm_'+str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'pvalue'])