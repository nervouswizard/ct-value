from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
#ct值=p值-0.5
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

        
        benign_count = 0
        malicious_count = 0
        for label in data['label']:
            if label == _benign:
                benign_count += 1
            else:
                malicious_count += 1
        if benign_count>=malicious_count:
            ratio = malicious_count/benign_count
        else:
            ratio = benign_count/malicious_count
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
            #多的平衡數量 =多的數量 x (少/多)
            #P= 多的平衡數量 / (多的平衡數量+少的數量)
            # = 多的數量 x (少/多) / (多的數量 x (少/多)+少的數量)
            p_b = b.copy()
            p_m = m.copy()
            for val, freq in b.items():
                if benign_count>malicious_count:
                    b_ratio = b[val] * ratio
                    p_b[val] = b_ratio / (b_ratio + m[val])
                else:
                    p_b[val] = b[val]  / bm_raw_counter[val]
                    
            for val, freq in m.items():
                if malicious_count>benign_count:
                    m_ratio = m[val] * ratio
                    p_m[val] = m_ratio / (m_ratio + b[val])
                else:
                    p_m[val] = m[val]  / bm_raw_counter[val]
            
            b_pvalue_df = pd.DataFrame.from_dict(p_b, orient='index').reset_index()
            m_pvalue_df = pd.DataFrame.from_dict(p_m, orient='index').reset_index()
        
            # 儲存map table
            b_pvalue_df.to_csv(os.path.join(save_path, '1_statistic', '2_map_table', filename,
            'b_'+str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'pvalue'])
            m_pvalue_df.to_csv(os.path.join(save_path, '1_statistic', '2_map_table', filename,
            'm_'+str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'pvalue'])