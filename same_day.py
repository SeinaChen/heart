#-*- coding:utf-8 
import time
t1 = time.time()
import pandas as pd
import numpy as np
from readfile import select_doc
from readfile import turned_sleep
from readfile import sleep_schedule
from readfile import heart_schedule
from readfile import Doc_processing
from normalize import heart_range
from normalize import h_range
from normalize import normal_heartbit
from normalize import new_h_time_normal
from normalize import new_heart_schedule
from readfile import get_month
month = get_month(1)
#csvファイルの読み込み
#month = ["March","April","May","June","July"]

#処理された文書集合 [0 sleep ,1 heart],[month select],[0 new_s_time|new_h_time, 1 new_s_day | new_h_day]
Doc_total = Doc_processing(1)

#heart schedule [month]
normal_new_h_time = new_heart_schedule(1)

#(1)日付重複確認
def check_repeated(ls):
    samemonth_date_group = []
    for x in ls:
        if x not in samemonth_date_group:
            samemonth_date_group.append(x)
    return samemonth_date_group


#(2)日付とtag dict
def date_tag(num):
    dict_date_zone_s =dict([[i,v]for i,v in enumerate(check_repeated(Doc_total[0][num][1]))])#日付分類タグ(sleep)
    dict_date_zone_h =dict([[i,v]for i,v in enumerate(check_repeated(Doc_total[1][num][1]))])#日付分類タグ(heart)
    result = (dict_date_zone_s,dict_date_zone_h)
    return result

#date_tag集合=>dict_date_zone_s ------- total_date_tag[num][0]
total_date_tag = [date_tag(num) for num in range(len(month))]

#(3)sleep and heart 共同日付
def same_date(num):
    ls_1 = [k for k in total_date_tag[num][0].values()]
    ls_2 = [k for k in total_date_tag[num][1].values()]
    date_same = [i for i in ls_1 if i in ls_2] #heart,sleep both date
    return date_same

#sleep and heart 共同日付集合 [month]
total_same_date = [same_date(num) for num in range(len(month))]

#(4)共同日付の各タグ(sleep,heart)
def same_tag(num):
    key_s_tag=[]
    key_h_tag=[]
    for i in list(total_same_date[num]):
        key_s = [k for k, v in total_date_tag[num][0].items() if v == i]#sleep
        key_h = [k for k, v in total_date_tag[num][1].items() if v == i]#heart
        key_s_tag.append(key_s)#sleep
        key_h_tag.append(key_h)#heart
    new_key_s_tag = [flatten for inner in key_s_tag for flatten in inner]
    new_key_h_tag = [flatten for inner in key_h_tag for flatten in inner]
    same_tag_ls = [(new_key_s_tag[i],new_key_h_tag[i]) for i in range(len(total_same_date[num]))]
    return same_tag_ls  #seelp[0],heart[1]
#共同日付の各タグ(sleep,heart)集合 [month]
total_same_tag = [same_tag(num) for num in range(len(month))]

def get_total(count):
    text = total_same_tag * count
    return text

#(5)日付に基づいて分類
#日付に基づいて分類(decided by tag)-sleep
def date_tag_s(num):
    new_schedule_s = []
    for i in Doc_total[0][num][0]:
        for n,j in enumerate(check_repeated(Doc_total[0][num][1])):
            if i[0] == j:
                new_schedule_s.append((n,i[0],i[2],i[3]))#num->同じ日付を指定している （日付分類[0]、日付[1]、処理された時間[2],睡眠状態[3])
    return new_schedule_s

#new_schedule_s集合
total_datetag_s = [date_tag_s(num) for num in range(len(month))]

def get_sleep(count):
    text = total_datetag_s * count
    return text

##############################################################
#日付に基づいて分類(decided by tag)-heart
def date_tag_h(num):
    new_schedule_h = []
    for i in normal_new_h_time[num]:
        for n,j in enumerate(check_repeated(Doc_total[1][num][1])):
            if i[0] == j:
                new_schedule_h.append((n,i[0],i[2],i[3]))#num->同じ日付を指定している （日付分類[0]、日付[1]、処理された時間[2],ハートビット[3])
    return new_schedule_h

#new_schedule_h集合 動けない
total_datetag_h = [date_tag_h(num) for num in range(len(month))]

def get_heart(count):
    text = total_datetag_h * count
    return text

#(6)同じ日付の各時間時間帯(30分)の４８等分
#time_zone = [((i,i+0.5),(i+1-0.5,i+1)) for i in range(24)]
#new_time_zone = [n for i in time_zone for n in i]
#dict_time_zone = dict([[v,n] for n,v in enumerate(new_time_zone)])#time_zone対応するタグ
#同じ日付の各時間時間帯(1h)の24等分
time_zone = [(i,i+1) for i in range(24)]
dict_time_zone = dict([[v,n] for n,v in enumerate(time_zone)])
print(dict_time_zone)
def value_range(num):#対応時間帯、対応時間
    for i in dict_time_zone.items():
        if i[0][0] <= num <= i[0][1]:
            return (i[1],num)

t2 = time.time()
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}秒")

