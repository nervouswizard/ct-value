# ct-value
python project of implement ct-value
## 前處理資料格式
資料須為.csv檔案 名稱不限 有多個csv檔案也可以 但須放在同一資料夾底下

資料建議放在data/1_preprocess

csv檔案不能有行號(row), 第一行須為column name

column name內不能包含特殊字元ex: \ / ? " * | < >

最後一個column name須為'label'

與 label 直接相關的 column , 例如 'attack_cat' 或 'label-detail' 之類的 要在config.ini內設定

## sample 部分
所有採樣完的 csv 檔案 label 幾乎都是1:1

採樣前假設 label A與label B 數量為6:4

採樣label B 的所有資料

將 label A 以隨機採樣方式採取至 A:B 為 1:1 -> random_data

將 label A 以 column['sum'] 高到低採取至 A:B 為 1:1 -> top20_data

top20_data 的 label A 的資料再增加一些沒採取到的 feature 分布 -> HQSC_data
