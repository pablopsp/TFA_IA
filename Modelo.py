import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

excelData = pd.read_excel('data/Ibex35Data.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in excelData.values()]
data = dict(excelData)

X = data['ACCIONA'][['Var.(€)', 'Var.(%)', 'Máx', 'Mín', 'Volumen(€)']]
Y = data['ACCIONA'][['Cierre']]

X_train = np.array(X[:int(0.7*len(X))])
Y_train = np.array(Y[:int(0.7*len(Y))])

X_test = np.array(X[int(0.7*len(X)):])
Y_test = np.array(Y[int(0.7*len(Y)):])

regr = linear_model.LinearRegression()
regr.fit(X_train, Y_train)
print('slope:', regr.coef_)