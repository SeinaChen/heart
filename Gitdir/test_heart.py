#-*- coding:utf-8
import pandas as pd
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
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

#元の心臓数
origin_heart = processing(df_ls[0])
print("######",len(origin_heart))

#Origin
heart_num = len(origin_heart)
heart = [(datetime.datetime.strptime(origin_heart[i][0], '%Y-%m-%d %H:%M:%S'),origin_heart[i]) for i in range(heart_num)]
#heart = [origin_heart[i] for i in range(heart_num)]
df_heart = pd.DataFrame(heart,columns=['time', 'heart'])

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

heart_matrix = df_heart['time']
heart_array = [t[1] for t in df_heart['heart'].values]
#print(heart_array)
matrix_len = len(heart_array)

#usr,date,time,heart
matrix = [(d,str(heart_matrix[i].date()),time_processing(str(heart_matrix[i].time())),int(heart_array[i])) for i in range(matrix_len)]
print(len(matrix))

import sqlite3
conn = sqlite3.connect("health.db")
conn.executemany("insert into heart values(?,?,?,?)", matrix)

cur = conn.cursor()
cur.execute( "select * from heart" )
list = cur.fetchall()
print( list )

conn.commit()
conn.close()
