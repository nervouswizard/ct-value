import os
import pandas as pd

def map_testset(file_path, save_path, label_column, print=print):
    test = pd.read_csv(file_path, low_memory=False)

    column_list = test.columns.to_list()
    map_path = os.path.join('data', '2_score', 'statistic', 'map_table')

    # 對每個feature找對應的map表，將值替換為p值
    pvalue_test = test.copy()
    # 對每個feature找對應的map表，將值替換為benign的ct值
    benign_test = test.copy()

    # p值缺值補0.5，ct值缺值補0
    for c, col in enumerate(column_list):
        if col in label_column: continue
        print(f'replace {c} {col}')
        map_df = pd.read_csv(os.path.join(map_path, str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
        pvalue_test[col] = pvalue_test[col].map(map_df.set_index('value')['pvalue']).fillna(0.5).astype(float)
        benign_test[col] = pvalue_test[col] - 0.5
        del map_df
    pvalue_test.to_csv(os.path.join(save_path, 'pvalue_test.csv'), index=None)
    benign_test.to_csv(os.path.join(save_path, 'benign_test.csv'), index=None)