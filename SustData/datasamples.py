import pandas as pd
import numpy as np
import glob as gl
from tqdm import tqdm


#DATETIME_SAMPLE = '2011-07-01' #d2
#DATETIME_SAMPLE = '2013-01-01' #d3
DATETIME_SAMPLE = '2014-01-01' #d4
HOUR_SAMPLE = 0

path = gl.glob('dataset/preprocessed/new_power_samples_d4*.csv')
dfs = [pd.read_csv(file, low_memory=False) for file in path] #lectura de todos los .csv
df = pd.concat(dfs, ignore_index=True) #df con todos los dfs


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
def extract_mean(IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE):
    filter = df[(df['iid'] == IID_SAMPLE) & (df['H'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
    filter.head()

    df = pd.DataFrame() #df de almacenamiento
 
    for feature in tqdm(X_features, desc=f'Procesando IID {IID_SAMPLE}'):
        if feature == 'iid':
            df[feature] = IID_SAMPLE
        else:
            df[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return df  
  

################################################################################################################
#función de cálculo de la media del total de valores de Pavg en un período de tiempo 
################################################################################################################
def Pavg_mean(IID_SAMPLE, DATETIME_SAMPLE):
    filter = df[(df['iid'] == IID_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
    filter.head()

    df = pd.DataFrame() #df de almacenamiento
 
    for feature in tqdm(X_features, desc=f'Procesando IID {IID_SAMPLE}'):
        if feature == 'iid':
            df[feature] = IID_SAMPLE
        else:
            df[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return df  



iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
print(iid_array) 

""" extraction = [extract_mean(iid, HOUR_SAMPLE, DATETIME_SAMPLE) for iid in iid_array] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
new_df.to_csv('OUT.csv', index=False) """



media = Pavg_mean(42, DATETIME_SAMPLE)
media.head()