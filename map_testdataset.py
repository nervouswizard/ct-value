import os
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def draw_confusion_matrix(test_y, preds, t):
    cm=confusion_matrix(test_y, preds)
    plt.figure(figsize=(8,8))
    plt.title(t,fontsize=28)
    sns.heatmap(cm,square=True,annot=True,fmt='d',linecolor='white',cmap='Greens',linewidths=1.5,cbar=False)
    plt.xlabel('HS',fontsize=20)
    plt.ylabel('True',fontsize=20)
    plt.savefig(os.path.join(save_path, f"{t}.png"))
    
save_path = os.path.join('data', '6_mapped_test')
os.makedirs(save_path, exist_ok=True)

print('Loading data ...')

filename = os.path.join('data', '0_ori' ,'1-1_tst.csv')
test = pd.read_csv(filename, low_memory=False)
del filename

column_list = test.columns.to_list()
drop_column = ['label']
map_path = os.path.join('data', '2_score', '1_statistic', '2_map_table', '1-1_trn')
count_path = os.path.join('data', '2_score', '2_weight',  '1-1_trn')
# 對每個feature找對應的map表，將值替換為benign的ct值
benign_test = test.copy()
for c, col in enumerate(column_list):
    if col in drop_column: continue
    print(f'replace {c} {col}')
    map_df = pd.read_csv(os.path.join(map_path, 'b_'+str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
    #count_df = pd.read_csv(os.path.join(count_path, str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
    #map_df.loc[count_df['count'] <= 3, 'pvalue'] = 0.5
    map_df['pvalue'] = map_df['pvalue']-0.5
    benign_test[col] = benign_test[col].map(map_df.set_index('value')['pvalue']).fillna(0).astype(float)
    del map_df
benign_test.to_csv(os.path.join(save_path, 'benign_test.csv'), index=None)


# 對每個feature找對應的map表，將值替換為malicious的ct值
malicious_test = test.copy()
for c, col in enumerate(column_list):
    if col in drop_column: continue
    print(f'replace {c} {col}')
    map_df = pd.read_csv(os.path.join(map_path, 'm_'+str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
    #count_df = pd.read_csv(os.path.join(count_path, str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
    #map_df.loc[count_df['count'] <= 3, 'pvalue'] = 0.5
    map_df['pvalue'] = map_df['pvalue']-0.5
    malicious_test[col] = malicious_test[col].map(map_df.set_index('value')['pvalue']).fillna(0).astype(float)
    del map_df
malicious_test.to_csv(os.path.join(save_path, 'malicious_test.csv'), index=None)

# 將值替換為對應label的ct值
# cheat_test = test.copy()
# for c, col in enumerate(column_list):
#     if col in drop_column: continue
#     print(f'replace {c} {col}')

#     benign_map_df = pd.read_csv(os.path.join(map_path, 'b_'+str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
#     benign_map_df['pvalue'] = benign_map_df['pvalue']-0.5
#     benign_map_dict = benign_map_df.set_index('value')['pvalue'].to_dict()
#     del benign_map_df

#     malicious_map_df = pd.read_csv(os.path.join(map_path, 'm_'+str(c)+'_'+column_list[c]+'.csv'), low_memory=False)
#     malicious_map_df['pvalue'] = malicious_map_df['pvalue']-0.5
#     malicious_map_dict = malicious_map_df.set_index('value')['pvalue'].to_dict()
#     del malicious_map_df

#     cheat_test[test['label']==0.0][col].replace(benign_map_dict, inplace=True)
#     cheat_test[test['label']==1.0][col].replace(malicious_map_dict, inplace=True)

#     cheat_test.loc[~cheat_test[col].isin(list(benign_map_dict.values())+list(malicious_map_dict.values())), col] = 0

# cheat_test.to_csv(os.path.join(save_path, 'cheating_test.csv'), index=None)

# 將值替換為sum比較高的類別的的ct值
test = benign_test.copy()

malicious_sum = malicious_test.drop(columns=drop_column, inplace=False).sum(axis=1)
benign_sum = benign_test.drop(columns=drop_column, inplace=False).sum(axis=1)

compare = malicious_sum>benign_sum

draw_confusion_matrix(test['label'].to_numpy(), compare.to_numpy(), 'map')

test[compare] = malicious_test[compare]

test.to_csv(os.path.join(save_path, 'HS_test.csv'), index=None)