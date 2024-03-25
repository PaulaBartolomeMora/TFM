import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras 
from scikeras.wrappers import KerasClassifier
import glob as gl
import os

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import time
import seaborn as sns

##############################################################

path = "src/results"
dfs = []

for file in gl.glob(path + '/20*.csv'):
    dfs.append(pd.read_csv(file))

df = pd.concat(dfs, ignore_index=True)

modelo = df.iloc[:, 8].values 
modelo = LabelEncoder().fit_transform(modelo) #codificación del modelo
datetime = df.iloc[:, 14].values 
datetime = LabelEncoder().fit_transform(datetime) #codificación del datetime

df = df.drop(df.columns[[8, 14]], axis=1) #se eliminan las antiguas con los strings del modelo y datetime
df['modelo'] = modelo #se añade la nueva codificada al final
df['datetime'] = datetime #se añade la nueva codificada al final

X = df.iloc[:, 1:] 
X = X.drop(['timestamp', 'load', 'DC Array Output (W)' , 'Pavg', 'dif'], axis=1)
y = df.iloc[:, 0].values #valores de overflow

##############################################################

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

sc = StandardScaler() #escalado de datos
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

##############################################################

parameters = {
    #'hidden_layer_sizes': [(10,), (50,), (100,), (10, 10), (50, 50)], 
    'hidden_layer_sizes': [(5,), (8,), (5, 5), (8, 8)], 
    'activation': ['relu', 'tanh'],  # Función de activación
    'solver': ['sgd', 'adam'],  # Algoritmo de optimización
}

mlp = MLPClassifier(max_iter=100, verbose=True, early_stopping=True, tol=0.00001)
grid_search = GridSearchCV(mlp, parameters, cv=5)

inigs = time.time()
grid_search.fit(X, y)
fings = time.time()

print("Precisión: %f con parámetros %s" % (grid_search.best_score_, grid_search.best_params_))
print("Tiempo ejecución grid search: " + str(fings-inigs))
print("\n--------------------------\n")
print(grid_search.cv_results_)

for mean, std, param in zip(grid_search.cv_results_['mean_test_score'], 
                            grid_search.cv_results_['std_test_score'], 
                            grid_search.cv_results_['params']):
    print("%f || %f --- %r" % (mean, std, param)) 
    