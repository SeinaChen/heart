import pandas as pd
df = pd.read_csv('new13_test.csv')
X = df[['normal_heart','step']].values
y = df['process_sleep'].values

def data_predict(num):
    result = (X,y) * num
    return result
print(len(data_predict(1)[0]))
