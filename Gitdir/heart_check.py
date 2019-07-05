#-*- coding:utf-8
import pandas as pd
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from check_sleep import new_matrix
import datetime

#実験者ID
z = input("被験者ID：")
d = int(z)

#日付(年+月)
x = input("ファイル番号：")
Document_ls = ['{0}heart'.format(x)]
a = int(x[0:4])
b = int(x[4:6])

#月毎に日付数
y = input("一ヶ月の日数:")
c = int(y)

def processing(df):
    ls = [(df['ExaminedAt'][i],df['Val1'][i]) for i in range(len(df))]
    return ls

df_ls = [pd.read_csv('/Users/xinnanchen/Desktop/201905predict/ID{0}/ReadData/'.format(d) +i+'.csv',sep =',') for i in Document_ls]

#正規化計算
def zscore(x):
    xmean = np.mean(x)
    xstd = np.std(x)
    zscore = [round(((x[i]-xmean)/xstd),3) for i in x]
    return zscore

#元の心臓数
origin_heart = processing(df_ls[0])


#正規化された心臓数
normal_heart = zscore([i[1] for i in origin_heart])
heart_num = len(normal_heart)

heart = [(datetime.datetime.strptime(origin_heart[i][0], '%Y-%m-%d %H:%M:%S'), normal_heart[i]) for i in range(heart_num)]


#時間,正規化された心臓数のみ #datetime,sleep
df_heart = pd.DataFrame(heart, columns=['time', 'heart'])

###################
#######照合########
###################

#####
#sleep => date, time 0~540, sleep
df_ts = new_matrix() #date,time,sleep

#heart
heart_matrix = df_heart['time']
heart_array = df_heart['heart'].values
matrix_len = len(heart_array)

def time_processing(a):
    ls = a.split(":") # matrix[i] => [0],[1]
    total = int(ls[0])*60+ int(ls[1]) #[0] hour*60 , [1] min
    if total % 5 == 0:
        result = total
    elif (total-1) % 5 == 0:
        result = total - 1
    else:
        result = total + 1
    return result


#heart => date, time 0~540, normalized heart
matrix = [(str(heart_matrix[i].date()),time_processing(str(heart_matrix[i].time())),heart_array[i]) for i in range(matrix_len)]
print("#####",matrix)

#照合リスト
time_array = [] #usr,date,time,sleep,heart
for i in matrix:
    for t in df_ts:
        if i[0] == t[0]:
            if i[1] == t[1]:
                time_array.append((d,t[0],t[1],int(t[2]),i[2])) #0:usr,1:date,2:time,3:sleep,4:heart

print("##########FINAL RESULT##############")  

#print(time_array)

new_date = set([i[1] for i in time_array])

date_array = [(d,i) for i in new_date]
#print(date_array)


#####health DB接続,table: time_line######
#import sqlite3
#conn = sqlite3.connect("health.db")
#conn.executemany("insert into time_line values(?,?,?,?,?)", time_array)
#conn.executemany("insert into date_line values(?,?)", date_array)
#conn.executemany("insert into heart values(?,?,?,?)", heart_array)

#cur = conn.cursor()
#cur.execute( "select * from date_array" )
#list = cur.fetchall()
#print( list )
 
#conn.commit()
#conn.close()
