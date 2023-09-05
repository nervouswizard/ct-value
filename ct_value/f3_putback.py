import os, sys
import pandas as pd

def putback(file_path_data, read_path_pvalue, save_path, label_column, print=print):
    os.makedirs(os.path.join(save_path, 'p-value'), exist_ok=True)
    os.makedirs(os.path.join(save_path, 'ct-value'), exist_ok=True)
    # 讀檔
    # pvalue data
    Pdata = pd.read_csv(file_path_data, low_memory=False)
    # CTvalue data
    #CTdata = pd.read_csv(file_path_data, low_memory=False)
    CTdata = Pdata.copy()
    pvaluePath = os.path.join(read_path_pvalue, 'statistic', 'map_table')
    '''
    for c, col in enumerate(Pdata.columns.to_list()):
        if col in label_column: continue
        print("Process", c, col)

        #將csv變成dict {'value': p-value}
        pvalueDataFilenameByColunm = os.path.join(pvaluePath,str(c)+'_'+col+'.csv')
        pvalueDF = pd.read_csv(pvalueDataFilenameByColunm, header=0, low_memory=False)
        print('benign P-value Data Shape', pvalueDF.shape)

        #將csv變成dict {'value': p-value}
        tmpDitc = pvalueDF.to_dict(orient='list')
        pvalueDict = dict()
        for i in range(len(tmpDitc['value'])):
            pvalueDict[tmpDitc['value'][i]] = tmpDitc['pvalue'][i]

        #將原本csv內的值改為p_value
        for i in range(len(Pdata.index)):
            feature = Pdata.at[i, col]
            Pdata.at[i, col] = pvalueDict.get(feature, 0)
            CTdata.at[i, col] = Pdata.at[i, col]-0.5
    '''
    for c, col in enumerate(Pdata.columns.to_list()):
        if col in label_column: continue
        print(f'replace {c} {col}')
        pvalueDataFilenameByColunm = os.path.join(pvaluePath,str(c)+'_'+col+'.csv')
        pvalueDF = pd.read_csv(pvalueDataFilenameByColunm, header=0, low_memory=False)
        print('benign P-value Data Shape', pvalueDF.shape)
        Pdata[col] = Pdata[col].map(pvalueDF.set_index('value')['pvalue']).fillna(0).astype(float)
        CTdata[col] = Pdata[col] - 0.5
        del pvalueDF
    #存檔
    Pdata.to_csv(os.path.join(save_path, 'p-value', 'train.csv'), index=None)
    CTdata.to_csv(os.path.join(save_path, 'ct-value', 'train.csv'), index=None)