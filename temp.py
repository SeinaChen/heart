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
from same_day import check_repeated
from same_day import date_tag
from same_day import same_date
from same_day import same_tag
from same_day import get_total
from same_day import get_sleep
from same_day import get_heart
from same_day import date_tag_s
from same_day import date_tag_h
from same_day import value_range

#(1)sleep処理
total_same_tag = get_total(1)
month_tag = [i for i,v in enumerate(total_same_tag) if len(v)!= 0]
print("##",month_tag)#->空集を削除
total_datetag_s = get_sleep(1)
x_s = []
for num in month_tag:
    total_s = []
    per_day_s = []
    date_n_s = [w[0] for w in total_same_tag[num]]
    for i in total_datetag_s[num]:#月分選択
        for w in date_n_s:
            if i[0] == w:
                total_s.append(w)
                per_day_s.append((value_range(i[2])[0],w,i[3])) #時間帯タグ、日付タグ、睡眠状態  
        s = [[n for n in per_day_s if n[1]==i] for i in date_n_s]
    x_s.append(s)


#(2)heart処理
total_datetag_h = get_heart(1)
x_h = []#=>x_h[0]month[date][0]
for num in month_tag:
    total_h = []
    per_day_h = []
    date_n_h = [w[1] for w in total_same_tag[num]]
    for i in total_datetag_h[num]:#change it ! because total is a little different ??????    for w in date_n_h:
        for w in date_n_h:
            if i[0] == w:
                total_h.append(w)
                per_day_h.append((value_range(i[2])[0],w,i[3]))
    h = [[n for n in per_day_h if n[1]==i] for i in date_n_h]
    x_h.append(h)

#(3)sleepに関するmatrix num1->month num2->date
def new_Matrix_s(num1,num2):
    w_s, h_s = 3, 48;
    Matrix_s = [[0 for x in range(w_s)] for y in range(h_s)]
    for i, v in enumerate(Matrix_s):
        for n in x_s[num1][num2]:#->日付変換
            if n[0] == i and n[2] == 0:
                v[0] += 1
            elif n[0] == i and n[2] == 1:
                v[1] += 1
            elif n[0] == i and n[2] == 2:
                v[2] += 1
    new_Matrix_s = Matrix_s #print(Matrix) 時間ごとに、matrix(時間帯0~48番目、睡眠状態Matrix[0]sports,[1]light,[2]deep)
    return new_Matrix_s

#####################################################
#(4)heartに関するmatrix num1->month num2->date
def new_Matrix_h(num1,num2):
    w_h, h_h = 1, 48;
    Matrix_h = [[0 for x in range(w_h)] for y in range(h_h)]
    for i, v in enumerate(Matrix_h):
        for n in x_h[num1][num2]:#->日付変換
            if n[0] == i:
                v.append(n[2])

    #0を補足した行列-heart
    new_Matrix_h = []
    for i,v in enumerate(Matrix_h):
        if len(v) <7:
            v = v+[0]*(7-len(v))
            new_Matrix_h.append(v)
        else:
            v = v
            new_Matrix_h.append(v)

        #1番目の0要素を削除
    for i in new_Matrix_h:
        i.pop(0)
    return new_Matrix_h

#毎日のデータの取得
def shmatrix(num1,num2):
    w_s = new_Matrix_s(num1,num2)
    w_h = new_Matrix_h(num1,num2)
    return (w_s,w_h)


total_compaire_ls = []
for num1 in range(len(x_s)):
    month_compaire_ls = []
    for num2 in range(len(x_s[num1])):
        day_compaire_ls = []
        for i in range(48):
            day_compaire_ls.append((shmatrix(num1,num2)[0][i],shmatrix(num1,num2)[1][i]))
        month_compaire_ls.append(day_compaire_ls)
    total_compaire_ls.append(month_compaire_ls)

def total_compaire(count):
    ls = total_compaire_ls * count
    return ls

def get_monthcompaire(num):
    ls_flatten = [flatten for inner in total_compaire_ls[num] for flatten in inner]
    return ls_flatten
