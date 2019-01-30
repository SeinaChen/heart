import pandas as pd
import numpy as np
from test import data_predict
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression

#######TEST_DATA#######
TEST_DATA = data_predict(1)
TEST_X = TEST_DATA[0]
TEST_Y = TEST_DATA[1]
print(len(TEST_X))
print(len(TEST_Y))
#######TEST_DATA#######

df = pd.read_csv('new.csv')
X = df[['normal_heart','step']].values
y = df['process_sleep'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
print("===========Result=============")
#k-近傍法
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train, y_train)
# knn.scoreで正解率を算出。
print("knn手法train score:",knn_model.score(X_train,y_train))
print("###knn手法test score:",knn_model.score(X_test,y_test))

#予測　
Y_pred_knn = knn_model.predict(TEST_X)
# 平方根平均二乗誤差（RMSE）
knn_rmse = np.sqrt(mean_squared_error(TEST_Y,Y_pred_knn))
print("誤差",knn_rmse)
print("予測値",Y_pred_knn)
print("実際値",TEST_Y)
print("\n")
###################
#決定木
DTC_model = DecisionTreeClassifier(max_depth=3)
DTC_model.fit(X_train, y_train)
#DTC.scoreで正解率を算出。
print("DTC手法train score:",DTC_model.score(X_train,y_train))
print("###DTC手法test score:",DTC_model.score(X_test,y_test))

#予測
Y_pred_DTC = DTC_model.predict(TEST_X)
# 平方根平均二乗誤差（RMSE）
DTC_rmse = np.sqrt(mean_squared_error(TEST_Y,Y_pred_DTC))
print("誤差",DTC_rmse)
print("予測値",Y_pred_DTC)
print("実際値",TEST_Y)
print("\n")
###################
#SVM
SVM_model = LinearSVC()
SVM_model.fit(X_train, y_train)
#SVM.scoreで正解率を算出。
print("SVM手法train score:",SVM_model.score(X_train,y_train))
print("###SVM手法test score:",SVM_model.score(X_test,y_test))

#予測
Y_pred_SVM = SVM_model.predict(TEST_X)
# 平方根平均二乗誤差（RMSE）
SVM_rmse = np.sqrt(mean_squared_error(TEST_Y,Y_pred_SVM))
print("誤差",SVM_rmse)
print("予測値",Y_pred_SVM)
print("実際値",TEST_Y)
print("\n")
###################
#ロジスティック回帰
Logis_model = LogisticRegression()
Logis_model.fit(X_train, y_train)
# Logis.scoreで正解率を算出。
print("Logistic回帰手法train score:",Logis_model.score(X_train,y_train))
print("###Logistic回帰手法test score:",Logis_model.score(X_test,y_test))

#予測
Y_pred_logis = Logis_model.predict(TEST_X)
# 平方根平均二乗誤差（RMSE）
Logis_rmse = np.sqrt(mean_squared_error(TEST_Y,Y_pred_logis))
print("誤差",Logis_rmse)
print("予測値",Y_pred_logis)
print("実際値",TEST_Y)
print("\n")
print("===========Result=============")

import math
import numpy as np
from matplotlib import pyplot

Y_fact = TEST_Y
Y_knn = Y_pred_knn
Y_DTC = Y_pred_DTC
Y_SVM = Y_pred_SVM
Y_Log = Y_pred_logis

x = [i for i in range(len(Y_fact))]
pyplot.plot(x, Y_fact, color='red',  linestyle='solid', linewidth = 3.0, label='fact')
pyplot.plot(x, Y_knn, label='knn')
pyplot.plot(x, Y_DTC, label='DTC')
pyplot.plot(x, Y_SVM, label='SVM')
pyplot.plot(x, Y_Log, label='Logistic')

pyplot.yticks([-2,-1, 0, 1, 2])
pyplot.xticks([0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300])

pyplot.title('User13 test result',loc='left')

pyplot.xlabel('X-データ順番')
pyplot.ylabel('Y-目的変数')

#グラフの凡例
pyplot.legend()

pyplot.show()
