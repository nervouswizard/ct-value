from collections import Counter
import pandas as pd
import os
#ct值=p值-0.5
def score(file_path, save_path, label_column, print=print):
    # 讀檔
    print(file_path)
    data = pd.read_csv(file_path)
    column_list = data.columns.to_list()

    os.makedirs(os.path.join(save_path, 'statistic', 'map_table'), exist_ok=True)

    benign_count = 0
    malicious_count = 0
    for label in data['label']:
        if label == 0:
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
        data = pd.read_csv(file_path, usecols=[col, 'label'], low_memory=False)
        
        # 特徵值出現的次數
        feature_counts = Counter(data[column_list[c]])

        benign = data[data['label'] == 0]
        b = Counter(benign[column_list[c]])

        # pvalue(相對於benign)，在benign出現越多次，pvalue越靠近1
        pvalue = {}
        for key, value in feature_counts.items():
            pvalue[key] = b[key] / value
        
        balance_pvalue = {}
        for key, value in feature_counts.items():
            # 平衡數量
            balance_pvalue[key] = pvalue[key] * ratio / (pvalue[key] * ratio + (1 - pvalue[key]))
            

        pvalue_df = pd.DataFrame.from_dict(balance_pvalue, orient='index').reset_index()

        # 儲存map table
        pvalue_df.to_csv(os.path.join(save_path, 'statistic', 'map_table',
        str(c)+'_'+column_list[c]+'.csv'), index=None, header=['value', 'pvalue'])