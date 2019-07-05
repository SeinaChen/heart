#-*- coding:utf-8
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
from same_day import date_tag_s
from same_day import date_tag_h
from same_day import value_range
from temp import new_Matrix_s
from temp import new_Matrix_h
from temp import shmatrix
from temp import total_compaire
from temp import get_monthcompaire 

range_num = len(total_compaire(1)) #=> range(len(ls))
#range_num 月を表示
test_compaire_ls = [get_monthcompaire(num) for num in range(range_num)] #
compaire_ls = [flatten for inner in test_compaire_ls for flatten in inner]

#不要データの削除
new_compaire_ls = []
for i,v in enumerate(compaire_ls):
    if sum(v[0])!= 0 and sum(v[1])!=0 and len(v[1]) <7:
        new_compaire_ls.append((i,v))#時間帯、睡眠状態、ハートビット

dict_check_matrix = dict([[i[0],i[1]] for i in new_compaire_ls])#時間帯、いらないデータを除いたmatrix
X_1 = [i[1][1]for i in new_compaire_ls]
sleep_Y = [i[1][0]for i in new_compaire_ls]

#睡眠状態確認(0 sports,1 light, 2 deep)
predict_sleep = []
for i,v in enumerate(sleep_Y):
    if sum(v) == 0:
        sleep_degree = 0.0
        predict_sleep.append(sleep_degree)
    else:
        sleep_degree = (v[0]*0+v[1]*1+v[2]*2)/sum(v)
        predict_sleep.append(round(sleep_degree,2))

Y_1 = predict_sleep
predict_model_data = [X_1[i]+[Y_1[i]] for i in range(len(X_1))]

#(2)モデルデータ
def get_data(count):
    data_model = predict_model_data * count
    return data_model
print(get_data(1))
