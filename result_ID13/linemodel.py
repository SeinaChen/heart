import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv('new.csv')
print(df.head())

#特徴量(説明変数)ベクトルの作成
X = df[['step','normal_heart']].values

#(目的変数)ベクトル
y = df['process_sleep'].values

#データ分割&&線形回帰
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
#clf = LogisticRegression(C=100).fit(X_train, y_train.astype('int'))
clf = LinearRegression()
clf.fit(X_train,y_train)

#トレーニングに使用したデータセットでの精度
print("トレーニング精度",clf.score(X_train,y_train))

#テストに使用したデータセットでの精度
print("テスト精度",clf.score(X_test,y_test))

#モデルの評価
print(clf.coef_)
print(clf.intercept_)
print(clf.score(X,y))

#平均二乗誤差を評価するためのメソッドを呼び出し
#from sklearn.metrics import mean_squared_error
#学習用、検証用データに関して平均二乗誤差を出力
#print('MSE Train : %.3f, Test : %.3f' % (mean_squared_error(y_train, y_train_pred), mean_squared_error(y_test, y_test_pred)))
