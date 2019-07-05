import pandas as pd
import numpy as np
import os
#csvファイルの読み込み
path = "/Users/xinnanchen/Desktop/data/"
Doc_ls = [path+i for i in os.listdir(path)]

month = ["March","April","May","June","July","August","Sep"]

X = input("ユーザーIDは:")
Document_h = ["/Users/xinnanchen/Desktop/data/User_"+X+"_{0}_h.csv".format(i) for i in month]
Document_s = ["/Users/xinnanchen/Desktop/data/User_"+X+"_{0}_s.csv".format(i) for i in month]

Do_h = [i for i in Document_h if i in Doc_ls]
Do_s = [i for i in Document_s if i in Doc_ls]

D_h = [[{i:n} for i in month if i in n]for n in Do_h]
D_s = [[{i:n} for i in month if i in n]for n in Do_s]

X_h = [((list((i[0].keys())))[0]) for i in D_h]
X_s = [((list((i[0].keys())))[0]) for i in D_s]

#heart,sleep 共同ある月
common = [i for i in X_h if i in X_s]

def get_month(count):
    month = common * count
    return month


#(1)
def select_doc(num):#num ->month
    #ファイル選択
    csv_input_h = pd.read_csv(Do_h[num])
    csv_input_s = pd.read_csv(Do_s[num])
    data_h = list(csv_input_h.values)#heartbit
    data_s = list(csv_input_s.values)#sleep
    doc_total = (data_s,data_h) #sleep 0,heart 1
    return doc_total   

#文書集合
Document_total = [select_doc(num) for num in range(len(common))] #[month][sleep0|heart1][id][character]

#(2)睡眠データ状態の変換(1->deep,2->light,3->sports = (2->deep, 1->light, 0->sports))
#睡眠2018/11/15 1,2=>1 sleep | 0=>sport
def turned_sleep(num):#num ->month
    new_s = [i[7] for i in Document_total[num][0]] #jupyter data_s -> Document_total[num][0] | data_h -> Document_total[num][1]
    s = []#変換後sleep状態データ
    for i in new_s:
        if i == 3:
            new_i = 0 #sports
            s.append(new_i)
        elif i == 2:
            new_i = 1 #light
            s.append(new_i)
        else:
            new_i = 1 #deep
            s.append(new_i) 
    return s

#変換した睡眠集合
sleep_total = [turned_sleep(num) for num in range(len(common))] #[month]total

#(3)睡眠
def sleep_schedule(num):
    new_s_time = [(Document_total[num][0][i][2].split(" ")[0],Document_total[num][0][i][2].split(" ")[1],round((int(Document_total[num][0][i][2].split(" ")[1].split(":")[0]) + int(Document_total[num][0][i][2].split(" ")[1].split(":")[1])/60),2),sleep_total[num][i]) for i in range(len(Document_total[num][0]))] #睡眠測る時間
    new_s_day = [Document_total[num][0][i][2].split(" ")[0] for i in range(len(Document_total[num][0]))]#[2]は実験日付
    result = (new_s_time,new_s_day)
    return result
#睡眠集合
sleep_schedule_total = [sleep_schedule(num) for num in range(len(common))] #[month][new_s_time0 | new_s_day1][id][character]


#(4)heartbit
def heart_schedule(num):
    new_h_time = [(Document_total[num][1][i][2].split(" ")[0],Document_total[num][1][i][2].split(" ")[1],round((int(Document_total[num][1][i][2].split(" ")[1].split(":")[0]) + int(Document_total[num][1][i][2].split(" ")[1].split(":")[1])/60),2),Document_total[num][1][i][7]) for i in range(len(Document_total[num][1]))] #睡眠測る時間
    new_h_day = [Document_total[num][1][i][2].split(" ")[0] for i in range(len(Document_total[num][1]))]#[2]は実験日付
    result = (new_h_time,new_h_day)
    return result
#heartbit集合
heart_schedule_total = [heart_schedule(num) for num in range(len(common))] #[month][new_h_time0 | new_h_day1][id][character]

#(5)処理された文書集合
def Doc_processing(num):
    result = (sleep_schedule_total,heart_schedule_total)*num
    return result

