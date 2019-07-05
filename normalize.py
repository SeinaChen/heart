import pandas as pd
import numpy as np
from readfile import select_doc
from readfile import turned_sleep
from readfile import sleep_schedule
from readfile import heart_schedule
from readfile import Doc_processing
from readfile import get_month
month = get_month(1)
#csvファイルの読み込み
#month = ["March","April","May","June","July"]

#処理された文書集合 [0 sleep ,1 heart],[month select],[0 new_s_time|new_h_time, 1 new_s_day | new_h_day]
Doc_total = Doc_processing(1)
#print("heart schedule time",Doc_total[1][num][0]) -> example
#new_h_time Doc_total[1][num][0]

#(1)heartbit 正規する
def heart_range(ls):
    #heart_list(per_month_total_heart)
    heart_list = [i[3] for i in ls]
    #heart_bit_average平均
    h_average = sum(heart_list)/len(heart_list)
    #print("平均",h_average)
    #heart_bit_SD標準偏差
    h_SD = np.std(np.array(heart_list))
    #print("標準偏差",h_SD)
    #heartbit_range - per_person 範囲(正規化)
    h_range_max = int(h_average + h_SD*2)
    h_range_min = int(h_average - h_SD*2)
    result = (h_range_min,h_range_max,heart_list) #range_min[0],range_max[1],heart_list[2]
    return result

#(2)
def h_range(num):
    o_h_r_min = min(heart_range(Doc_total[1][num][0])[2])
    o_h_r_max = max(heart_range(Doc_total[1][num][0])[2])
    n_h_r_min = int((heart_range(Doc_total[1][num][0])[0]-heart_range(Doc_total[1][num][0])[0])/(heart_range(Doc_total[1][num][0])[1]-heart_range(Doc_total[1][num][0])[0]))
    n_h_r_max = int((heart_range(Doc_total[1][num][0])[1]-heart_range(Doc_total[1][num][0])[0])/(heart_range(Doc_total[1][num][0])[1]-heart_range(Doc_total[1][num][0])[0]))
    result1 = (o_h_r_min,o_h_r_max)
    result2 = (n_h_r_min,n_h_r_max)
    result =  [result1,result2]
    return result
#print("元範囲",h_range(0)[0][0],"~",h_range(0)[0][1]) #->h_range(month)
#print("正規化された範囲",h_range(0)[1][0],"~",h_range(0)[1][1])

#範囲集合
normal_range = [h_range(num) for num in range(len(month))] #[month可変量][元0|正規1][min0|max1]

#(3)heartbit正規化
def normal_heartbit(num):
    new_heart_list = []
    #各数値を正規化する
    for i in heart_range(Doc_total[1][num][0])[2]:
        n = (i-normal_range[num][0][0])/(normal_range[num][0][1]-normal_range[num][0][0])
        n_i = n*(normal_range[num][1][1]-normal_range[num][1][0]) + normal_range[num][1][0]
        new_heart_list.append(round(n_i,2))
    return new_heart_list

#nomalized heartbit 集合
normal_total_heart = [normal_heartbit(num) for num in range(len(month))] #[month可変量]

#新しいheart schedule
#正規化配列 日付(0),時間(1),処理された時間(2),正規化ハートビット(3)
#(4)元heartbit => new_h_time[i][3]
def new_h_time_normal(num):
    result  = [(Doc_total[1][num][0][i][0],Doc_total[1][num][0][i][1],Doc_total[1][num][0][i][2],normal_total_heart[num][i]) for i in range(len(Doc_total[1][num][0]))]
    return result

#(5)新しいheart schedule集合
new = [new_h_time_normal(num) for num in range(len(month))] #[month可変量]
def new_heart_schedule(num):
    result = new*num
    return result

