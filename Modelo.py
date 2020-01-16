import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

excelData = pd.read_excel('data/Ibex35Data.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in excelData.values()]
data = dict(excelData)

def ModelCompanie(companieName):
    print("-----------------------------------------------")
    print("Companie: ", companieName)
    
    data[companieName] = data[companieName].apply(lambda x: x.str.replace(',','.'))
    data[companieName]['Volumen(€)'] = data['ACCIONA']['Volumen(€)'].apply(lambda x: x.replace('.',''))
    
    X = data[companieName][['Var.(€)', 'Var.(%)', 'Máx', 'Mín', 'Volumen(€)']]
    Y = data[companieName][['Cierre']]
    
    X_train = np.array(X[:int(0.7*len(X))])
    Y_train = np.array(Y[:int(0.7*len(Y))])
    
    X_test = np.array(X[int(0.7*len(X)):])
    Y_test = np.array(Y[int(0.7*len(Y)):])
    
    regr=linear_model.LinearRegression()
    regr.fit(X_train,Y_train)
    y_pred = regr.predict(X_train)
    
    t1=regr.coef_
    print('Pendiente: \n', t1)
    t0=regr.intercept_
    print('Término independiente: \n', t0)
    print('El modelo de regresión es: y = %f + %f * X1 +  %f * X2 + %f * X3 + %f * X4 + %f * X5'%(t0,t1[0][0],t1[0][1],t1[0][2], t1[0][3],t1[0][4]))
    print("ECM : %.2f" % mean_squared_error(Y_train, y_pred))
    # Puntaje de Varianza. El mejor puntaje es un 1.0
    print('Coeficiente Correlacción: %.2f' % r2_score(Y_train, y_pred))
    
    y_pred_test = regr.predict(X_test)
    
    # Error (pérdida)
    print("Error o pérdida del modelo de regresión lineal para valores de test")
    # Error Cuadrático Medio (Mean Square Error)
    print("ECM : %.2f" % mean_squared_error(Y_test, y_pred_test))
    # Puntaje de Varianza. El mejor puntaje es un 1.0
    print('Coeficiente Correlacción: %.2f' % r2_score(Y_test, y_pred_test))
    
    print("-----------------------------------------------")

    
[ModelCompanie(companie) for companie in data.keys()]
#ModelCompanie('ACCIONA')