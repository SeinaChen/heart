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
from final_matrix import shmatrix
from final_matrix import get_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from dataprocess import certificate_model

predict_model_data  = get_data(1)
df = pd.DataFrame(predict_model_data,columns=['heart1', 'heart2', 'heart3','heart4','heart5','heart6','sleep_state'])

#Xを作成
df_except = df.drop('sleep_state', axis=1)
X = df_except.values
#Yを作成
y = df['sleep_state'].values

# 70%を学習用、30%を検証用データにするよう分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
clf = LogisticRegression(C=100).fit(X_train, y_train.astype('int'))

def get_model(count):
    clf = LogisticRegression(C=100).fit(X_train, y_train.astype('int'))*count
    return clf

y_train_pred = clf.predict(X_train)#X_train入り変えの新しいデータの予測
y_test_pred = clf.predict(X_test)#モデルの評価

print("Training set score{:.2f}".format(clf.score(X_train,y_train.astype('int'))))
print("Test set score{:.2f}".format(clf.score(X_test,y_test.astype('int'))))
# 回帰係数
#print("clf.coef_:{}".format(clf.coef_))
# 切片 (誤差)
#print("clf.intercept_:{}".format(clf.intercept_))
# 決定係数
#print(clf.score(X, y))

#平均二乗誤差を評価するためのメソッドを呼び出し
from sklearn.metrics import mean_squared_error
#学習用、検証用データに関して平均二乗誤差を出力
print('MSE Train : %.3f, Test : %.3f' % (mean_squared_error(y_train, y_train_pred), mean_squared_error(y_test, y_test_pred)))

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
logreg = LogisticRegression()
kfold = KFold(n_splits=5,shuffle=True,random_state=0)
scores = cross_val_score(logreg,X,y.astype('int'),cv = kfold, scoring ="neg_mean_squared_error")
print("Cross-validation scores:{}".format(scores))
print("Number of cv iterations:", len(scores))
print("Average cross-validition score:{:.2f}".format(abs(scores.mean())))

