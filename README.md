# ct-value
python project of implement ct-value
## 更新內容
要轉換成ct值的訓練資料須檔名須為train.csv，只能處裡單一檔案，須將train.csv放到 data\1_preprocess 內

相對應的訓練資料檔名須為test.csv，須將test.csv放到 data\1_preprocess 內

欄位label限定只能是0或1，data\1_preprocess內有檔案可以參考

計算完的訓練集檔案會存放在 data\3_DataWithPvalue 有p-value跟ct-value兩種版本

對應的測試集檔案會存放在 data\6_mapped_test 有p-value跟ct-value兩種版本

有增加sum欄位在最後一個column(label column之後)的檔案分別放在

data\4_sum、data\7_sum_test

## 前處理資料格式
csv檔案不能有行號(row), 第一行須為column name

column name內不能包含特殊字元ex: \ / ? " * | < >

建議可以換成 .

最後一個column name須為'label'

與 label 直接相關的 column, 或是不想參與計算ct值的column

例如 'attack_cat' 或 'label-detail' 之類的 要在config.ini內設定

## 5_sample 部分
所有採樣完的 csv 檔案 label 幾乎都是1:1

採樣前假設 label A與label B 數量為6:4

採樣label B 的所有資料

將 label A 以隨機採樣方式採取至 A:B 為 1:1 -> random_data

將 label A 以 column['sum'] 高到低採取至 A:B 為 1:1 -> top20_data

top20_data 的 label A 的資料再增加一些沒採取到的 feature 分布 -> HQSC_data
