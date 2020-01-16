import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

excelData = pd.read_excel('data/Ibex35Data.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in excelData.values()]
data = dict(excelData)


def ModelCompanie(companieName):
    print("-----------------------------------------------")
    print("Companie: ",companieName)
    
    data[companieName] = data[companieName].apply(lambda x: x.str.replace(',','.'))
    data[companieName]['Volumen(€)'] = data[companieName]['Volumen(€)'].apply(lambda x: x.replace('.',''))
    
    X = data[companieName][['Var.(€)', 'Var.(%)', 'Máx', 'Mín', 'Volumen(€)']]
    Y = data[companieName][['Cierre']]
    
    X_train = np.array(X[1:int(0.7*len(X))])
    Y_train = np.array(Y[1:int(0.7*len(Y))])
    
    X_test = np.array(X[int(0.7*len(X)):])
    Y_test = np.array(Y[int(0.7*len(Y)):])
    
    poli_reg = PolynomialFeatures(degree = 2)
    
    X_train_poli = poli_reg.fit_transform(X_train)
    X_test_poli = poli_reg.fit_transform(X_test)
    
    pr = linear_model.LinearRegression()
    pr.fit(X_train_poli, Y_train)
    Y_pred_pr = pr.predict(X_test_poli)
    
    print("ECM : %.2f" % mean_squared_error(Y_test, Y_pred_pr))
    print('Coeficiente Correlacción: %.2f' % r2_score(Y_test, Y_pred_pr))
    print('Valor de la intersección o coeficiente "b": ', pr.intercept_)
    print('Precisión del modelo: ', pr.score(X_train_poli, Y_train))
    print("-----------------------------------------------")
    
#[ModelCompanie(companie) for companie in data.keys()]
ModelCompanie('ACCIONA')