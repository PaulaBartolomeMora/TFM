import pandas as pd
import numpy as np


DATETIME_SAMPLE = '2013-01-01'
HOUR_SAMPLE = 0

dataset = 'dataset/preprocessed/new_power_samples_d3_1split_2.csv'
df = pd.read_csv(dataset)  

#parseo de timestamp y creación de nueva columna H
df['tmstp'] = pd.to_datetime(df['tmstp'])
df['H'] = df['tmstp'].dt.strftime('%H') #nueva columna de hora
df['H'] = df['H'].astype(int)

#extracción de features
X = df.iloc[:, 3:18] #names + values
X_features = X.columns.to_list() #names to list
X_features.append('iid')


################################################################################################################
#función de cálculo de la media del total de valores medidos en una hora determinada para un nodo determinado
################################################################################################################
def extract(IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE):
    filter = df[(df['iid'] == IID_SAMPLE) & (df['H'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
    filter.head()

    hourly_data = pd.DataFrame() #df de almacenamiento

    for feature in X_features:
        if feature == 'iid':
            hourly_data[feature] = IID_SAMPLE
        else:
            hourly_data[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return hourly_data    


iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
# print(iid_array) 

extraction = [extract(iid, HOUR_SAMPLE, DATETIME_SAMPLE) for iid in iid_array] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
new_df.to_csv('OUT.csv', index=False)