import os, sys
import pandas as pd

def putback(read_path_data, read_path_pvalue, save_path, label_column, _malicious, print=print):
    os.makedirs(os.path.join(save_path, 'p-value'), exist_ok=True)
    os.makedirs(os.path.join(save_path, 'ct-value'), exist_ok=True)
    os.makedirs(os.path.join(save_path, 'wct-value'), exist_ok=True)
    # 讀檔
    for i, filename in enumerate(os.listdir(read_path_data)):
        if not filename.endswith('.csv'): continue
        print(i, filename)
        # pvalue data
        Pdata = pd.read_csv(os.path.join(read_path_data, filename), low_memory=False)
        # CTvalue data
        CTdata = pd.read_csv(os.path.join(read_path_data, filename), low_memory=False)
        # WCTvalue data
        WCTdata = pd.read_csv(os.path.join(read_path_data, filename), low_memory=False)

        pvaluePath = os.path.join(read_path_pvalue, '1_statistic', '2_map_table')
        weigthPath = os.path.join(read_path_pvalue, '2_weight')

        for c, col in enumerate(Pdata.columns.to_list()):
            if col in label_column: continue
            print("Process", c, col)

            #將csv變成dict {'value': p-value}
            filename = filename.replace('.csv', '/')
            weigthDataFilenameByColunm = os.path.join(weigthPath,filename+str(c)+'_'+col+'.csv')
            weigthDF = pd.read_csv(weigthDataFilenameByColunm, header=0, low_memory=False, usecols=['value', 'count'])
            wDict = weigthDF.to_dict(orient='list')
            pvalueDataFilenameByColunm = os.path.join(pvaluePath,filename+'b_'+str(c)+'_'+col+'.csv')
            pvalueDF = pd.read_csv(pvalueDataFilenameByColunm, header=0, low_memory=False)
            print('benign P-value Data Shape', pvalueDF.shape)
            tmpDitc = pvalueDF.to_dict(orient='list')
            bDict = dict()
            
            for i in range(len(tmpDitc['value'])):
                '''
                if wDict['count'][i] <= 3:
                    bDict[tmpDitc['value'][i]] = 0.5
                else:
                    bDict[tmpDitc['value'][i]] = tmpDitc['pvalue'][i]
                '''
                bDict[tmpDitc['value'][i]] = tmpDitc['pvalue'][i]

            #將csv變成dict {'value': p-value}
            pvalueDataFilenameByColunm = os.path.join(pvaluePath,filename+'m_'+str(c)+'_'+col+'.csv')
            pvalueDF = pd.read_csv(pvalueDataFilenameByColunm, header=0, low_memory=False)
            print('malicious P-value Data Shape', pvalueDF.shape)
            tmpDitc = pvalueDF.to_dict(orient='list')
            mDict = dict()
            
            for i in range(len(tmpDitc['value'])):
<<<<<<< HEAD
                if wDict['count'][i] <= 3:
=======
                '''
                if wDict['count'][i]  <= 3:
>>>>>>> sample
                    mDict[tmpDitc['value'][i]] = 0.5
                else:
                    mDict[tmpDitc['value'][i]] = tmpDitc['pvalue'][i]
                '''
                mDict[tmpDitc['value'][i]] = tmpDitc['pvalue'][i]
            #將csv變成dict {'value': weigth}
            
            weigthDataFilenameByColunm = os.path.join(weigthPath,filename+str(c)+'_'+col+'.csv')
            weigthDF = pd.read_csv(weigthDataFilenameByColunm, header=0, low_memory=False, usecols=['value', 'weight'])
            print('weight P-value Data Shape', weigthDF.shape)
            tmpDitc = weigthDF.to_dict(orient='list')
            weigth = dict()

            for i in range(len(tmpDitc['value'])):
                weigth[tmpDitc['value'][i]] = tmpDitc['weight'][i]

            #將原本csv內的值改為p_value
            for i in range(len(Pdata.index)):
                feature = Pdata.at[i, col]
                if Pdata.at[i, 'label'] == _malicious:
                    Pdata.at[i, col] = mDict.get(feature, 0)
                    CTdata.at[i, col] = (mDict.get(feature, 0)-0.5)
                    WCTdata.at[i, col] = (mDict.get(feature, 0)-0.5) * weigth.get(feature, 0)
                else:
                    Pdata.at[i, col] = bDict.get(feature, 0)
                    CTdata.at[i, col] = (bDict.get(feature, 0)-0.5)
                    WCTdata.at[i, col] = (bDict.get(feature, 0)-0.5) * weigth.get(feature, 0)

        #存檔
        filename = filename.replace('/', '')
        Pdata.to_csv(os.path.join(save_path, 'p-value',filename+'.csv'), index=None)
        CTdata.to_csv(os.path.join(save_path, 'ct-value',filename+'.csv'), index=None)
        WCTdata.to_csv(os.path.join(save_path, 'wct-value',filename+'.csv'), index=None)
