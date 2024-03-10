
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import glob as gl
import os

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC 
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE, SelectKBest, chi2
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix, accuracy_score

import time

##############################################################

path = "src/results"
dfs = []

for file in gl.glob(path + '/20*.csv'):
    dfs.append(pd.read_csv(file))

df = pd.concat(dfs, ignore_index=True)

modelo = df.iloc[:, 8].values 
modelo = LabelEncoder().fit_transform(modelo) #codificación del modelo
df = df.drop(df.columns[8], axis=1) #se elimina la antigua con los strings del modelo
df['modelo'] = modelo #se añade la nueva codificada al final

X = df.iloc[:, 1:] 
X = X.drop(['datetime', 'timestamp', 'load', 'DC Array Output (W)' , 'Pavg', 'dif'], axis=1)
y = df.iloc[:, 0].values #valores de overflow

##############################################################

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

sc = StandardScaler() #escalado de datos
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

##############################################################

#APLICACIÓN PCA
#pca2 = PCA(n_components=2)
pca3 = PCA(n_components=3)
#X_train_pca2 = pca2.fit_transform(X_train)
#X_test_pca2 = pca2.transform(X_test)
X_train_pca3 = pca3.fit_transform(X_train)
X_test_pca3 = pca3.transform(X_test)

##############################################################

""" #APLICACIÓN FEATURE SELECTION, ESTO YA ESTÁ EJECUTADO

scaler = MinMaxScaler() # Escalar las características al rango [0, 1]

select_feature = SelectKBest(chi2, k=8).fit(scaler.fit_transform(X_train), y_train) 
selected_features = X.columns[select_feature.get_support(indices=True)]
print('Selected features:', selected_features)

X_train_fs = select_feature.transform(X_train)
X_test_fs = select_feature.transform(X_test)"""

##############################################################

#inicl = time.time()
classifier = SVC(kernel = 'rbf', random_state = 0)
#classifier.fit(X_train, y_train)
#fincl = time.time()

#print("Tiempo ejecución clasificador 1: " + str(fincl-inicl))  """

##############################################################

""" ESTO YA ESTÁ EJECUTADO
# Importancia de las características basada en la distancia a los vectores de soporte

support_vectors = classifier.support_vectors_ #vectores de soporte
dual_coef = classifier.dual_coef_ #multiplicadores de Lagrange asociados
print("Vectores soporte y coeficientes: ")
print(support_vectors)
print(dual_coef)

importances = np.abs(np.dot(dual_coef, support_vectors)).flatten()
importances_series = pd.Series(importances, index=X.columns)
plt.figure(figsize=(10, 6))
importances_series.plot(kind='bar')
plt.ylabel('Importancia')
plt.title('Importancia de las características del SVC con kernel RBF')
plt.xticks(rotation=45, ha='right')
plt.show() """

##############################################################

""" 
# Feature importance based on mean decrease in impurity --> #ESTO DA ERROR, SVC NO DEJA OBTENERLO ASÍ
features_ranking = pd.Series(classifier.feature_importances_, index=X.columns)

plt.figure(figsize=(10, 6))  
features_ranking.plot(kind='bar')
plt.ylabel('Importancia')
plt.title('Importancia de las características del RF a partir de la Disminución Media de la Impureza (MDI)')
plt.xticks(rotation=45, ha='right')
plt.show() """

##############################################################

# Feature importance based on feature permutation --> ESTO YA SE HA EJECUTADO

""" result = permutation_importance(
    classifier, X_test, y_test, n_repeats=5, random_state=42, n_jobs=2
)

importances_mean_series = pd.Series(result.importances_mean, index=X.columns)

plt.figure(figsize=(10, 6))
importances_mean_series.plot(kind='bar')
plt.ylabel('Importancia')
plt.title('Importancia de las características del RF a partir de la permutación')
plt.xticks(rotation=45, ha='right')
plt.savefig('importance4.png', bbox_inches='tight')
plt.show() """

##############################################################

#APLICACIÓN RFE Y RFECV NO SE PUEDE CON SVC, NO TIENE ATRIBUTO feature_importances_)

""" print("Ejecutando RFE")

rfe = RFE(estimator=classifier, n_features_to_select=5, step=1)  
rfe = rfe.fit(X_train, y_train)

print('Ranking de features :', rfe.ranking_)
print('Mejores features :', X.columns[rfe.support_]) """








##############################################################
##############################################################
##############################################################

""" ##CM
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(cm) 
accuracy_score(y_test, y_pred)

##K-FOLD
accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation: {:.2f} %".format(accuracies.std()*100)) """

##############################################################

""" ##CM
y_pred = classifier.predict(X_test_pca2)
cm = confusion_matrix(y_test, y_pred)
print(cm) 
accuracy_score(y_test, y_pred)

inicl = time.time()
classifier.fit(X_train_pca2, y_train) 
fincl = time.time()
print("Tiempo ejecución clasificador 2: " + str(fincl-inicl)) 

##K-FOLD
accuracies = cross_val_score(estimator = classifier, X = X_train_pca2, y = y_train, cv = 10)
print("Accuracy PCA 2: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation PCA 2: {:.2f} %".format(accuracies.std()*100))  """

##############################################################

y_pred = classifier.predict(X_test_pca3)
cm = confusion_matrix(y_test, y_pred)
print(cm) 
accuracy_score(y_test, y_pred)

""" inicl = time.time()
classifier.fit(X_train_pca3, y_train) 
fincl = time.time()
print("Tiempo ejecución clasificador 3: " + str(fincl-inicl)) 

accuracies = cross_val_score(estimator = classifier, X = X_train_pca3, y = y_train, cv = 10)
print("Accuracy PCA 3: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation PCA 3: {:.2f} %".format(accuracies.std()*100))  """

##############################################################
##############################################################
##############################################################








##GRID SEARCH

""" parameters = [{'C': [0.25, 0.5, 0.75, 1], 'kernel': ['linear']},
              {'C': [0.25, 0.5, 0.75, 1], 'kernel': ['rbf']}]

processors = 32
cv = 5 
combos = 1

for i in parameters:
    for j in i.values():
        combos *= len(j)

num_models = combos * cv / processors 
seconds = num_models * (fincl-inicl)
minutes = seconds / 60
hours = minutes / 60

print("{:.6f}".format(hours), "| {:.6f}".format(minutes), "| {:.6f}".format(seconds))


inigs = time.time()

print("Ejecutando Grid Search")

grid_search = GridSearchCV(estimator = classifier,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 5,
                           n_jobs = -1)

grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_
print("Best Accuracy: {:.2f} %".format(best_accuracy*100))
print("Best Parameters:", best_parameters)
print(grid_search.best_estimator_)
print(grid_search.cv_results_) 

fings = time.time()

print("Tiempo ejecución grid search: " + str(fings-inigs))

print("Imprimiendo reporte")

y_pred_gs = grid_search.predict(X_test) 
print(classification_report(y_test, y_pred_gs))  """