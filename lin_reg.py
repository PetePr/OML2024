# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:08:25 2024

@author: Admin
"""
import numpy as np
import scipy as sp
from sklearn.linear_model import LinearRegression
import pandas as pd
from math import sqrt, sin, cos, pi
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def data_gen(X, a, noise, mean, variance, beta):
    n = X.shape[0]
    y = np.zeros((n, 1))
    if (X.shape[1] + 1) != a.shape[0]:
        print('Error: check dimensions')
    else:
        x0 = np.ones((n, 1))
        X0 = np.hstack((x0, X))
        y = X0@a
        if (noise == "normal"):
            for i in range(y.shape[0]):
                y[i] = y[i] + sp.stats.norm.rvs(mean, variance)
        elif (noise == "laplace"):
            for i in range(y.shape[0]):
                y[i] = y[i] + sp.stats.laplace.rvs(mean, variance)
        else:
            for i in range(y.shape[0]):
                y[i] = y[i] + sp.stats.gennorm.rvs(beta, mean, variance)
    return y


def calcfg_Lp_criterion(w, X, y, p):
    n = X.shape[0] # = y.shape[0], якщо X це numpy масив із shape=(n,d), y це numpy масив із shape=(n,1)
    d = X.shape[1]
    x0 = np.ones((n, 1))
    X0 = np.hstack((x0, X))
    F = 0
    g_F = np.zeros(d+1).reshape((d+1, 1))
    xi = y - (X0@w).reshape((1, n))
    F = np.sum(np.power(np.abs(xi), p))    

    if (p == 1):
        g_F[0] = np.sum(-np.abs(xi)*np.sign(xi))
        for i in range(1, d):
            g_F[i] = np.sum(-np.abs(xi)*np.sign(xi)*X[:, i])
    elif (p == 2):
       g_F[0] = np.sum(-2*xi)
       for i in range(1, d):
           g_F[i] = np.sum(-2*xi*X[:, i])
    elif (p > 1):
        g_F[0] = np.sum((-p)*np.power(np.abs(xi), p-1)*np.sign(xi))
        for i in range(1, d):
            g_F[i] = np.sum((-p)*np.power(np.abs(xi), p-1)*np.sign(xi)*X[:, i])
    else:
        print('Error - the value of p is < 1')

    return F, g_F

def elipsoid_method(calcfg, X, y, p,
                    w0,
                    r0,
                    epsf = 1e-6,
                    maxitn = int(1e6), intp = int(1e2)):
    # Initialization
    f_values = []  
    w_values = []
    n = len(w0)
    w = np.copy(w0)
    B = np.identity(n)
    r = r0
    beta = sqrt((n-1.0)/(n+1.0))

    # Main cycle
    w_values.append(w)
    for itn in range(maxitn):
        # Computation of f and g on a given iteration
        f, g1 = calcfg(w, X, y, p) #(w, X, y)
        f_values.append(f)
        g = np.copy(B.T @ g1)
        dg = np.linalg.norm(g)

        # Displaying information after every intp iterations
        if ((itn % intp == 0) and (itn <= maxitn)):
            print('itn = {0}, f = {1}'.format(itn, f))

        # Optimization procedure termination criteria
        if (r*dg < epsf):
            ist = 1
            print('Result:')
            print('ist = {0}, itn = {1}, f = {2}'.format(ist, itn, f))
            return w, f, itn, ist, w_values, f_values

        xi = np.copy((1.0/dg) * g)
        dw = np.copy(B @ xi)
        hs = r / (n+1.0)

        # Computation of an approximation
        w = np.copy(w - hs * dw)
        w_values.append(w)

        B = np.copy(B + (beta-1.0) * (B @ xi) @ xi.T)
        r = r / sqrt(1.0 - 1.0/n) / sqrt(1.0 + 1.0/n)

    # Критерій закінчення оптимізаційної процедури
    ist = 4
    print('Result:')
    print('ist = {0}, itn = {1}, f = {2}'.format(ist, itn, f))
    return w, f, itn, ist, w_values, f_values


df = pd.read_csv('Student_Performance.csv')
arr = df.to_numpy()
n = 100
d = arr.shape[1]
Xtest = arr[0:n]
for i in range(n): #  Convert Yes/No to 0/1
    if (Xtest[i, 2]=="Yes"):
        Xtest[i, 2] = 1 
    else:
        Xtest[i, 2] = 0

#mu = np.mean(Xtest[:, 5])
#sigma = sqrt(np.var(Xtest[:, 5]))
Ytest = Xtest[:, 5].reshape((n, 1))
Xtest = Xtest[:, 0:5]
At = np.array([[6], [3], [0.3], [5], [2.5], [2]])
Ygen = data_gen(Xtest, At, "normal", 3, 5, 1)

reg = LinearRegression().fit(Xtest, Ytest)

#elipsoid_method(calcfg_Lp_criterion, Xtest, Ytest, 2, w, 1, 1e-6, int(1e6), int(1e2))



