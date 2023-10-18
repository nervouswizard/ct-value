import os, csv
import pandas as pd
import numpy as np
from collections import Counter

def listtocsv(nanValuesList, path, col):
    if nanValuesList is []:
        return
    os.makedirs(path, exist_ok=True)
    nanValuesConter = Counter(nanValuesList)
    nanValuesConter = sorted(nanValuesConter.items(), key=lambda x: x[1], reverse=True)
    with open(os.path.join(path, col+'.csv'), 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, ['ori', 'count'])
        writer.writeheader()
        for v, c in nanValuesConter:
            writer.writerow({'ori': v, 'count': c})

def map_testset(file_path, save_path, label_column, print=print):
    test = pd.read_csv(file_path, low_memory=False)

    column_list = test.columns.to_list()
    map_path = os.path.join('data', '2_score', 'statistic', 'map_table')

    # 對每個feature找對應的map表，將值替換為p值
    pvalue_test = test.copy()
    # 對每個feature找對應的map表，將值替換為benign的ct值
    benign_test = test.copy()

    # 統計各column缺值總數
    total_massing = {}
    # p值缺值補0.5，ct值缺值補0
    for c, col in enumerate(column_list):
        if col in label_column: continue
        print(f'replace {c} {col}')
        pvalueDataFilenameByColunm = os.path.join(map_path, str(c)+'_'+col+'.npy')
        pvalueNParray = np.load(pvalueDataFilenameByColunm)
        pvalueSeries = pd.Series(pvalueNParray[1, :])
        pvalueSeries.index = pvalueNParray[0, :]
        
        pvalue_test[col] = pvalue_test[col].map(pvalueSeries).astype(float)
        # 統計缺值
        nanValuesList = test[col][pvalue_test[col].isna()].tolist()
        total_massing[col] = len(nanValuesList)
        listtocsv(nanValuesList, os.path.join(save_path, 'missing'), str(c)+'_'+col)
        # 缺值補0.5
        pvalue_test[col] = pvalue_test[col].fillna(0.5).astype(float)

        benign_test[col] = pvalue_test[col] - 0.5
        
    pvalue_test.to_csv(os.path.join(save_path, 'pvalue_test.csv'), index=None)
    benign_test.to_csv(os.path.join(save_path, 'benign_test.csv'), index=None)
    
    df_len = len(test)
    with open(os.path.join(save_path, 'missing', 'total.csv'), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['column', 'count', 'proportion'])
        writer.writeheader()
        for v, c in total_massing.items():
            writer.writerow({'column': v, 'count': c, 'proportion': (c / df_len)*100})
