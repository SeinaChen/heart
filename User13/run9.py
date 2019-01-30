#-*- coding:utf-8
import pandas as pd
#Document_ls = ['step']
Document_ls = ['heart9','sleep9','step9']

def processing(df,date,a,b):
  date_time= [[i] for i in df['ExaminedAt'].tolist()]
  new_time= [(i[0].split(' ')[0],i[0].split(' ')[1]) for i in date_time]
  s_vl= [str(i) for i in df['Val1'].tolist()]
  new= [(new_time[i][0],new_time[i][1],s_vl[i]) for i in range(len(date_time))]
  day_time = [(i[1],i[2]) for i in new if i[0] == "2018-09-"+ date]
  hour_line = [(int((i[0].split(":"))[0])+int((i[0].split(":"))[1])/60,int(i[1])) for i in day_time] 
  hour_count = [i[1] for i in hour_line if a <= i[0] < b ] 
  int_val = [i for i in hour_count]
  #final_val= round(sum(int_val)/len(int_val),1)
  return int_val

df_ls = [pd.read_csv(i+'.csv',sep =',') for i in Document_ls]

date_ls = ['0'+str(i+1) for i in range(9)]
date_ls.extend([str(i+1) for i in range(9,30)])

hour_ls = [(0.25*i,0.25*i+0.25) for i in range(96)]

time_total = [(i,t) for i in date_ls for t in hour_ls]
#print(time_total)

print("\n","##########")
final_ls = []
for num,t in enumerate(df_ls):
  #print(num)
  new_ls = []
  for i in time_total: #time_total i[0][0]month | i[0][1]date | i[1][0]rangeA | i[1][1]rangeB
    v = processing(t,i[0],i[1][0],i[1][1])
    print("###",v)
    if len(v) != 0:
      final_val= round(sum(v)/len(v),1)
      new_ls.append(final_val)
    else:
      new_ls.append(0.0)
  final_ls.append(new_ls)

print(final_ls,len(final_ls))

print("#############################")
heart_ls = []
sleep_ls = []
step_ls = []
for num,i in enumerate(final_ls):
  if num == 0:
    heart_ls.append(i)
  elif num == 1:
    sleep_ls.append(i)
  else:
    step_ls.append(i)

#print("###",heart_ls[0],"\n")
#print("###",sleep_ls[0],"\n")
#print("###",step_ls[0],"\n")


datestr_ls = []#csv data 縦軸
for i in range(30):
  for t in range(96):
     string = "2018-09-"+str(i+1)+" "+str(0.25*t)+"時"
     datestr_ls.append(string)

#'heart','sleep','step'
new_df = pd.DataFrame({'heart': heart_ls[0],'sleep':sleep_ls[0],'step': step_ls[0]},index = datestr_ls)

data = new_df
print(new_df)
data.drop(data.index[data.heart == 0], inplace=True)
data.drop(data.index[(data.step == 0) & (data.sleep == 3)], inplace=True)
data.drop(data.index[data.step > 500], inplace=True)
data.drop(data.index[data.sleep == 0], inplace=True)

def df_data(count):
  result = new_df * count
  return result

# CSV ファイル (employee.csv) として出力
data.to_csv("/Users/xinnanchen/Desktop/datascience/result_ID13/result9.csv")

