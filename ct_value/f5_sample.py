import pandas as pd
import numpy as np
import os

def sample(file_path_ct, file_path_ori, save_path, label_column, sum_or_count01, print=print):
    # 讀CT值的csv檔案
    data = pd.read_csv(file_path_ct, low_memory=False)
    # 計算各label的數量
    label_counts = data['label'].value_counts().to_dict()
    print(label_counts)
    if len(label_counts) < 2: return
    min_label = min(label_counts[0], label_counts[1])

    # 保留較少數量的label，較多資料的label做之後的採樣
    if label_counts[0] > label_counts[1]:
        data_reserve = data[data['label'] != 'benign']
        data = data[data['label'] == 'benign']
    else:
        data_reserve = data[data['label'] == 'benign']
        data = data[data['label'] != 'benign']

    # 讀原始檔案
    ori_data = pd.read_csv(file_path_ori, low_memory=False)
    ori_data['label'] = ori_data['label'].replace(to_replace = ori_data['label'].unique()[1:], value = 'malicious')

    # 保留較少數量的label，較多資料的label做之後的採樣
    ori_data_reserve = ori_data.loc[data_reserve.index]
    ori_data = ori_data.loc[data.index]

    # 創建儲存資料夾
    
    # 初始化sample.txt
    with open(os.path.join(save_path, 'sample.txt'), mode='w') as f:
        pass

    # CT值分成20個區間
    interval_list = np.linspace(-0.5, 0.5, 20+1).tolist()
    
    # 刪除誤差，把數字四捨五入到四位小數
    interval_list = list([round(x, 4) for x in interval_list])

    # 隨機採樣最少數量label的個數
    random_data = data.sample(n=min_label, random_state=42)
    random_ori_data = ori_data.loc[random_data.index]

    # 隨機平衡label原始分布
    sample_data = pd.concat([random_ori_data, ori_data_reserve])
    sample_data.to_csv(os.path.join(save_path, 'ori_random_data.csv'), index=None)

    # 輸出隨機採樣CT分布
    sample_data = pd.concat([random_data, data_reserve])
    sample_data.to_csv(os.path.join(save_path, 'CT_random_data.csv'), index=None)

    # 依照sum的大小來排序
    if sum_or_count01 == 'sum':
        sorted_idx = data.sort_values(by='sum', ascending=False).index
    elif sum_or_count01 == 'count01':
        sorted_idx = data.sort_values(by='count_gt_0_1', ascending=False).index
    else:
        print('something wrong.please check config.ini :sum_or_count01')
        return
    data = data.reindex(sorted_idx)
    ori_data = ori_data.reindex(sorted_idx)

    # 使用CT值平衡label
    data_top_20_percent = data.head(min_label)
    ori_data_top_20_percent = ori_data.head(min_label)

    # 輸出使用CT值平衡label的CT分布
    sample_data = pd.concat([data_top_20_percent, data_reserve])
    sample_data.to_csv(os.path.join(save_path, 'CT_top20_data.csv'), index=None)

    # 輸出20%的原始分布
    sample_data = pd.concat([ori_data_top_20_percent, ori_data_reserve])
    sample_data.to_csv(os.path.join(save_path, 'ori_top20_data.csv'), index=None)

    # 使用CT值平衡label
    data_top_18_percent = data.head(min_label)

    # 原本資料筆數
    len_18_percent = len(data_top_18_percent)

    # data改為剩下的82%
    data = data.loc[~data.index.isin(data_top_18_percent.index)]
    
    # 每個區間至少要有的資料筆數
    thread1 = 1

    # 分20個區，對每個 feature 紀錄每個區間內出現次數
    for col in data_top_18_percent.columns:
        if col in label_column or col == 'sum' or col == 'count_gt_0_1': continue
        additional_data = []
        col_data = data_top_18_percent[col].values
        interval_counts, intervals = np.histogram(col_data, bins=interval_list)

        # 在剩下的82%中，把每個區間都補至少有thread筆
        for i, counts in enumerate(interval_counts):
            # 已經滿足的就跳過
            nees_counts = thread1 - counts
            if nees_counts <= 0: continue
            # 找出區間範圍
            interval_start, interval_end = intervals[i], intervals[i+1]
            # 這個feature所有的資料
            col_values = data[col].values
            # 找出在區間內的所有資料
            in_interval = (col_values >= interval_start) & (col_values <= interval_end)
            additional_data = data.loc[in_interval & ~data.index.isin(data_top_18_percent.index)]
            # 選資料的CT值最高的
            additional_data = additional_data.iloc[:nees_counts]
            # 找不到就跳過
            if len(additional_data) <= 0: continue
            
            data_top_18_percent = data_top_18_percent._append(additional_data, ignore_index=False)
            data = data.loc[~data.index.isin(additional_data.index)]

    # 輸出HQSC後CT分布
    sample_data = pd.concat([data_top_18_percent, data_reserve])
    sample_data.to_csv(os.path.join(save_path, 'CT_HQSC_data.csv'), index=None)

    # 輸出HQSC後原始分布
    ori_data_top_18_percent = ori_data.loc[data_top_18_percent.index]
    sample_data = pd.concat([ori_data_top_18_percent, ori_data_reserve])
    sample_data.to_csv(os.path.join(save_path, 'ori_HQSC_data.csv'), index=None)

    print("增加資料筆數：", len(data_top_18_percent)-len_18_percent)