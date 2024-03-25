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

def ann(): 
 
    model = keras.Sequential([
        
        #Adding the input layer and the first hidden layer
        #se prueba con 6, los valores se obtienen probando o con alguna técnica como k Fold Cross Validation
        keras.layers.Dense(7, input_shape=(X.shape[1],), activation='relu'), #nº de entradas
        
        #Adding the second hidden layer
        #mismo valor que arriba
        keras.layers.Dense(7, activation='relu'),
        
        #Adding the output layer -> 1 salida: 0 o 1
        #*si no es salida binaria, se indica el número de posibles salidas y activation='softmax'
        keras.layers.Dense(1, activation='sigmoid')
    ]) 

    #model.summary() #resumen de la estructura de la red neuronal
    #los parámetros son los pesos

    #inicl = time.time()

    model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    #History = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=2) 
    #fincl = time.time()

##############################################################

    """plt.figure(figsize=(10, 6))
    plt.plot(History.history['loss'])
    plt.title('Evolución de la función de pérdidas')
    plt.ylabel('Pérdidas')
    plt.xlabel('Epochs')
    plt.savefig('loss.png', bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(History.history['accuracy'])
    plt.title('Evolución de la precisión')
    plt.ylabel('Precisión')
    plt.xlabel('Epochs')
    plt.savefig('accuracy.png', bbox_inches='tight')
    plt.show() """

##############################################################

    """test_loss, test_accuracy = model.evaluate(X_test, y_test)

    y_pred = model.predict(X_test)
    y_pred = (y_pred > 0.5) #solución problema binario
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    accuracy_score(y_test, y_pred) """

    return model #,inicl,fincl


##############################################################
##############################################################
##############################################################

#m,inicl,fincl = ann()
#model = KerasClassifier(build_fn=ann)

"""
parameters = {
    'hidden_layer_sizes': [(5,5,1), (6,6,1), (7,7,1), (8,8,1)],
    'batch_size': [20, 50, 80],
    'epochs': [10, 20, 30, 40, 50],
    'activation': ['sigmoid', 'tanh', 'relu'],
}"""

""" batch_size = [20, 50, 80]
epochs = [10, 30, 50]
parameters = dict(batch_size=batch_size, epochs=epochs) """

parameters = {
    'batch_size': [20, 50, 80],
    'epochs': [10, 30, 50],
}

""" processors = 32
cv = 5 
combos = 1

for i in parameters:
    for j in i:
        combos *= len(j)

num_models = combos * cv / processors 
seconds = num_models * (fincl-inicl)
minutes = seconds / 60
hours = minutes / 60

print("{:.6f}".format(hours), "| {:.6f}".format(minutes), "| {:.6f}".format(seconds)) """

##############################################################

model = KerasClassifier(model=ann)

#param_grid = dict(batch_size=[20, 50, 80], epochs=[10, 30, 50])

inigs = time.time()
grid_search = GridSearchCV(estimator=model,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 5,
                           n_jobs = 1)

grid_search.fit(X_train, y_train)

fings = time.time()

print("Precisión: %f con parámetros %s" % (grid_search.best_score_, grid_search.best_params_))
print("Tiempo ejecución grid search: " + str(fings-inigs))
print("\n--------------------------\n")
print(grid_search.cv_results_)

for mean, std, param in zip(grid_search.cv_results_['mean_test_score'], 
                            grid_search.cv_results_['std_test_score'], 
                            grid_search.cv_results_['params']):
    print("%f || %f --- %r" % (mean, std, param)) 
    
    
#activation = ['softmax', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']