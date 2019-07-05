import pandas as pd
import glob
import numpy as np

csv_files = ["result13_test.csv"]

#print(csv_files)
list = []

for f in csv_files:
    list.append(pd.read_csv(f))
df = pd.concat(list)

#heart処理 正規化
#"0"を削除したheart_list
heart_ls = df['heart'].tolist()

#heartbit 正規する  X-平均/標準偏差
def S_heart_range(ls,i):
    #heart_list(per_month_total_heart)
    heart_list = ls
    #heart_bit_average平均
    h_average = sum(heart_list)/len(heart_list)
    #print("平均",h_average)
    #heart_bit_SD標準偏差
    h_SD = np.std(np.array(heart_list))
    #print("標準偏差",h_SD)
    #heartbit_range - per_person 範囲(正規化)
    X = (ls[i]- h_average) / h_SD
    return X

def M_heart_range(ls,i):  #選択した
    h_average = sum(ls)/len(ls)
    max_value = max(ls)
    min_value = min(ls)
    X = (ls[i] - min(ls))/(max(ls)-min(ls))
    return X

#result = [round(S_heart_range(heart_ls, i),2) for i in range(len(heart_ls))]
result = [round(M_heart_range(heart_ls, i),2) for i in range(len(heart_ls))]
#print(result)


#sleep処理
# 0 => 睡眠あり, 1 => 睡眠なし
# 1 深い睡眠, 2　浅い睡眠, 3 活動
sleep_ls = df['sleep'].tolist()
new = []
for i in sleep_ls:
    if i <= 2:
        x = 0
        new.append(x)
    else:
        x = 1
        new.append(x)

df['normal_heart'] = result
df['process_sleep'] = new
df.to_csv("new13_test.csv")

