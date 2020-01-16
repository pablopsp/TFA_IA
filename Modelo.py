import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_excel('data/Ibex35Data.xlsx', sheet_name=None)
[companie.drop(['Unnamed: 0'], axis='columns', inplace=True) for companie in data.values()]


fecha = []
cierre = []
varEuros = []
varPcntje = []
valMax = []
valMin = []
vol = []

for key in data.keys():
    fecha.append(data.get(key).get('Fecha'))
    cierre.append(data.get(key).get('Cierre'))
    varEuros.append(data.get(key).get('Var.(€)'))
    varPcntje.append(data.get(key).get('Var.(%)'))
    valMax.append(data.get(key).get('Máx'))
    valMin.append(data.get(key).get('Mín'))
    vol.append(data.get(key).get('Volumen(€)'))

cierreAux = []
varEurosAux = []
varPcntjeAux = []
valMaxAux = []
valMinAux = []
volAux = []
    
for i in range(len(cierre)):
    for k in range(len(cierre[i])):
        cierreAux.append(cierre[i][k])

for i in range(len(varEuros)):
    for k in range(len(varEuros[i])):
        varEurosAux.append(varEuros[i][k])

for i in range(len(varPcntje)):
    for k in range(len(varPcntje[i])):
        varPcntjeAux.append(varPcntje[i][k])

for i in range(len(valMax)):
    for k in range(len(valMax[i])):
        valMaxAux.append(valMax[i][k])

for i in range(len(valMin)):
    for k in range(len(valMin[i])):
        valMinAux.append(valMin[i][k])

for i in range(len(vol)):
    for k in range(len(vol[i])):
        volAux.append(vol[i][k])

# Asignamos las variables X (atributos) e y (etiquetas)
X=[varEurosAux,varPcntjeAux,valMaxAux,valMinAux,volAux]
y=[cierreAux]

# Dividimos el conjunto de datos para entrenamiento y test
# Elegimos a priori el 70 % para entrenamiento
# y el resto 30 % para test
limEnt = round(157787/100)*70
limTest = 157787 - limEnt

X_train = np.array(X[:110460])
y_train = np.array(y[:110460])
#X_test = np.array(X[limTest:])
#y_test = np.array(y[limTest:])

# Creamos el objeto de Regresión Lineal
regr=linear_model.LinearRegression()

# Entrenamos el modelo
regr.fit(X_train,y_train)

# Realizamos predicciones sobre los atributos de entrenamiento
y_pred = regr.predict(X_train)

# Recta de Regresión Lineal (y=t0+t1*X)
# Pendiente de la recta
t1=regr.coef_
print('Pendiente: \n', t1)
# Corte con el eje Y (en X=0)
t0=regr.intercept_
print('Término independiente: \n', t0)
# Ecuación de la recta
print('El modelo de regresión es: y = %f + %f * X1 +  %f * X2 + %f * X3'%(t0,t1[0][0],t1[0][1],t1[0][2]))

# Error (pérdida)
print("Error o pérdida del modelo de regresión lineal para valores de entrenamiento")
# Error Cuadrático Medio (Mean Square Error)
print("ECM : %.2f" % mean_squared_error(y_train, y_pred))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Coeficiente Correlacción: %.2f' % r2_score(y_train, y_pred))