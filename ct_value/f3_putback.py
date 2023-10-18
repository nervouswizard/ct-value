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

def putback(file_path_data, read_path_pvalue, save_path, label_column, print=print):
    os.makedirs(os.path.join(save_path, 'p-value'), exist_ok=True)
    os.makedirs(os.path.join(save_path, 'ct-value'), exist_ok=True)
    # 讀檔
    # pvalue data
    Pdata = pd.read_csv(file_path_data, low_memory=False)
    # CTvalue data
    CTdata = Pdata.copy()
    # 備份
    backup_Pdata = Pdata.copy()
    # 統計各column缺值總數
    total_massing = {}

    pvaluePath = os.path.join(read_path_pvalue, 'statistic', 'map_table')
    
    for c, col in enumerate(Pdata.columns.to_list()):
        if col in label_column: continue
        print(f'replace {c} {col}')
        pvalueDataFilenameByColunm = os.path.join(pvaluePath, str(c)+'_'+col+'.npy')
        pvalueNParray = np.load(pvalueDataFilenameByColunm)
        pvalueSeries = pd.Series(pvalueNParray[1, :])
        pvalueSeries.index = pvalueNParray[0, :]
        Pdata[col] = Pdata[col].map(pvalueSeries).astype(float)
        # 統計缺值
        nanValuesList = backup_Pdata[col][Pdata[col].isna()].tolist()
        total_massing[col] = len(nanValuesList)
        listtocsv(nanValuesList, os.path.join(save_path, 'missing'), str(c)+'_'+col)
        # 缺值補0.5
        Pdata[col] = Pdata[col].fillna(0).astype(float)

        CTdata[col] = Pdata[col] - 0.5
    #存檔
    Pdata.to_csv(os.path.join(save_path, 'p-value', 'train.csv'), index=None)
    CTdata.to_csv(os.path.join(save_path, 'ct-value', 'train.csv'), index=None)


    df_len = len(backup_Pdata)
    with open(os.path.join(save_path, 'missing', 'total.csv'), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['column', 'count', 'proportion'])
        writer.writeheader()
        for v, c in total_massing.items():
            writer.writerow({'column': v, 'count': c, 'proportion': (c / df_len)*100})