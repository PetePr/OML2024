# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:37:18 2024

@author: Admin
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import cross_val_score

df = pd.read_csv('day.csv')
df = df.drop('dteday', axis = 1)
df = df.drop([750, 751])
arr = df.to_numpy()

#X = arr[:, 0:12]
#Y = arr[:, 12:15]
#y1 = arr[:, 12]
#y2 = arr[:, 13]
#y3 = arr[:, 14]


X, y3 = make_regression(n_samples=500, n_features=30, n_informative=5)
reg0 = LinearRegression().fit(X, y3)
init_score = reg0.score(X, y3)
featureNames = SelectFromModel(reg0, prefit=True, max_features=5)
featureNames.fit(X, y3)
n = X.shape[0] # of samples
d = X.shape[1] # of features

scores1 = np.zeros(d)
for i in range(d):
    feature_i = X[:, i].reshape((n, 1))
    reg = LinearRegression().fit(feature_i, y3)
    scores1[i] = reg.score(feature_i, y3)
f1 = scores1.argmax(axis = 0)
#chosen1 = X[:, f1].reshape((n, 1))

X1 = np.delete(X, f1, 1)
scores2 = np.zeros(d-1)
for i in range(X1.shape[1]):
    add_feature_i = np.hstack((X1[:, i].reshape((n, 1)), X[:, f1].reshape((n, 1))))
    reg = LinearRegression().fit(add_feature_i, y3)
    scores2[i] = reg.score(add_feature_i, y3)
scores2 = np.insert(scores2, f1, 0)
f2 = scores2.argmax(axis = 0)
#chosen12 = X[:, [f1, f2]]

X2 = np.delete(X, [f1, f2], 1)
scores3 = np.zeros(d-2)
for i in range(X2.shape[1]):
    add_feature_i = np.hstack((X2[:, i].reshape((n, 1)), X[:, [f1, f2]]))
    reg = LinearRegression().fit(add_feature_i, y3)
    scores3[i] = reg.score(add_feature_i, y3)
F = [f1, f2]
F.sort()
scores3 = np.insert(scores3, F[0], 0)
scores3 = np.insert(scores3, F[1], 0)
f3 = scores3.argmax(axis = 0)

X3 = np.delete(X, [f1, f2, f3], 1)
scores4 = np.zeros(d-3)
for i in range(X3.shape[1]):
    add_feature_i = np.hstack((X3[:, i].reshape((n, 1)), X[:, [f1, f2, f3]]))
    reg = LinearRegression().fit(add_feature_i, y3)
    scores4[i] = reg.score(add_feature_i, y3)
F = [f1, f2, f3]
F.sort()
scores4 = np.insert(scores4, F[0], 0)
scores4 = np.insert(scores4, F[1], 0)
scores4 = np.insert(scores4, F[2], 0)
f4 = scores4.argmax(axis = 0)

X4 = np.delete(X, [f1, f2, f3, f4], 1)
scores5 = np.zeros(d-4)
for i in range(X4.shape[1]):
    add_feature_i = np.hstack((X4[:, i].reshape((n, 1)), X[:, [f1, f2, f3, f4]]))
    reg = LinearRegression().fit(add_feature_i, y3)
    scores5[i] = reg.score(add_feature_i, y3)
F = [f1, f2, f3, f4]
F.sort()
scores5 = np.insert(scores5, F[0], 0)
scores5 = np.insert(scores5, F[1], 0)
scores5 = np.insert(scores5, F[2], 0)
scores5 = np.insert(scores5, F[3], 0)
f5 = scores5.argmax(axis = 0)

Xfin = X[:, [f1, f2, f3, f4, f5]]
reg1 = LinearRegression().fit(Xfin, y3)
fin_score = reg1.score(Xfin, y3)





