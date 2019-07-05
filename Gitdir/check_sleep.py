#-*- coding:utf-8
import pandas as pd
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

z = input("被験者ID：")
d = int(z)

x = input("ファイル日付(例：201807):")
a = int(x[0:4])
b = int(x[4:6])

y = input("一ヶ月の日数:")
c = int(y)

Document_ls = ['{0}sleep'.format(x)]

def processing(df):
    ls = [(df['ExaminedAt'][i],df['Val1'][i]) for i in range(len(df))]
    return ls

df_ls = [pd.read_csv('/Users/xinnanchen/Desktop/201905predict/ID{0}/ReadData/'.format(d) +i+'.csv',sep =',') for i in Document_ls]

sleep = [(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S'), v) for t,v in processing(df_ls[0])]

df_sleep = pd.DataFrame(sleep, columns=['time', 'sleep'])

print(df_sleep)

#1,2含まれる部分を抽出
new_df = df_sleep[df_sleep['sleep'] != 3]
print(new_df['time']) #時間

df_ts = new_df['time']

matrix = []  ####useful####

for i in df_ts:
    matrix.append((str(i.date()),str(i.time())))

#睡眠値リスト
sleep_array = new_df['sleep'].values

#matrix [0]日付 [1]時間 睡眠時間処理 0~540
def time_processing(a):
    ls = a[1].split(":") # matrix[i] => [0],[1]
    total = int(ls[0])*60+ int(ls[1]) #[0] hour*60 , [1] min
    if total % 5 == 0:
        result = total
    elif (total-1) % 5 == 0:
        result = total - 1
    else:
        result = total + 1
    return result 

matrix_len = len(matrix)

#睡眠時間(heart時間　照合用) (date,time,sleep)
check_time = [(matrix[i][0],time_processing(matrix[i]),sleep_array[i]) for i in range(matrix_len)]
print(check_time)

######change########

def new_matrix():
    return check_time

######change########

ax = plt.subplot()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d\n%H:%M'))
ax.set_xlim(datetime.datetime(a, b, 1, 0), datetime.datetime(a, b, c, 23))
ax.set_ylim(0, 4)
ax.plot(df_sleep['time'], df_sleep['sleep'])
plt.xlabel('time')
plt.ylabel('sleep')
plt.title('{0}_ID{1}_sleep'.format(x,d))
plt.savefig('/Users/xinnanchen/Desktop/201905predict/ID{1}/{0}_ID{1}_sleep.png'.format(x,d))
plt.show()


