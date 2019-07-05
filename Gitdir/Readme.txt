Health Data  
|
|---health.db table <time_line(user,date,time,sleep,heart)> ①
|   |
|   |-heart_check.py => heart normalization, time(sleep_values:1,2)
|   |
|   |-check_sleep.py => sleep_values:1,2
|   |
|   |-Data(Total:14159, sleep:1,2)
|      |
|      |-ID11(201808~201901)
|      |-ID12(201805~201812)
|      |-ID13(201805~201812)
|
|---health.db table <sleep(user,date,time,sleep)>　② table <date_line(user,date)> ③
|      |
|      |-sup.py => sleep:1,2,3  if not time continous, sleep = 3 (check per day by table date_line)
|
|---health.db table <heart(user,date,time,heart)>　④ =>change avaliable (Nomalization: zscore | min-max)
|      |
|      |-test_heart.py => table sleep (1,2,3) 
|
|---health.db table <health(h1,h2,h3,s,h4,h5,h6)>　⑤
|      |
|      |-test_sleep.py=> continuous training data
|
|---health.db table <position(ID,ID,ID,ID,ID,ID,ID)>　⑥ => 頻度順にIDを付ける
|      |
|      |-health_corp.py=> continuous training data ID　(No.9  = 1| No.1   = 2 |No.8   = 3)
|
|---health_model(★MODEL★), pickle file　
|      |
|      |-learning_model.py=> continuous training data ID　
|
|--- TEST RESULT ??
|      |
|      |-prob_log.py
