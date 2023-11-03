import pandas as pd
import numpy as np


DATETIME_SAMPLE = '2013-01-01'
HOUR_SAMPLE = 0

dataset = 'dataset/preprocessed/new_power_samples_d3_1split_1.csv'
df = pd.read_csv(dataset)  
df.head()

#parseo de timestamp y creación de nueva columna H
df['tmstp'] = pd.to_datetime(df['tmstp'])
df['H'] = df['tmstp'].dt.strftime('%H') #nueva columna de hora
df['H'] = df['H'].astype(int)


################################################################################################################
#función de cálculo de la media del total de valores medidos en una hora determinada para un nodo determinado
################################################################################################################
def extract(IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE):
    filter = df[(df['iid'] == IID_SAMPLE) & (df['H'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
    filter.head()

    X = filter.iloc[:, 3:18] #se extraen columnas features -> nombre + valores
    X_features = X.columns.to_list()
    X_features.append('iid')
    X_values = X.values

    #print(X_features) #nombres features 
    #print(X_values) #valores features 

    hourly_data = pd.DataFrame() #df de almacenamiento
    array = np.array([])

    for feature in X_features:
        if feature == 'iid':
            hourly_data[feature] = IID_SAMPLE
        else:
            hourly_data[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return hourly_data
    


iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
# print(iid_array) 

data = []

for iid in iid_array:
    aux = extract(iid, HOUR_SAMPLE, DATETIME_SAMPLE)
    data.append(aux)

print(data)
