<<<<<<< HEAD
import pandas as pd
import numpy as np
import glob as gl
from tqdm import tqdm
import matplotlib.pyplot as plt


DATETIME_SAMPLE = '2011-07-01' #d2
#DATETIME_SAMPLE = '2013-01-01' #d3
#DATETIME_SAMPLE = '2014-01-01' #d4
HOUR_SAMPLE = 0

path = gl.glob('dataset/preprocessed/new_power_samples_d2*.csv') #power_samples -> OUT.csv
#path2 = gl.glob('NO/power_events/power_events_d2*.csv') #power_events -> OUT2.csv

dfs = [pd.read_csv(file, low_memory=False) for file in path] #lectura de todos los .csv
df = pd.concat(dfs, ignore_index=True) #df con todos los dfs


#parseo de timestamp y creación de nueva columna H
df['tmstp'] = pd.to_datetime(df['tmstp'])
df['H'] = df['tmstp'].dt.strftime('%H') #nueva columna de hora
df['H'] = df['H'].astype(int)


#extracción de features
#X = df.iloc[:, 3:18] #names + values
X = df.iloc[:, 3:4] #if power_events 
X_features = X.columns.to_list() #names to list
X_features.append('iid')


################################################################################################################
#función de cálculo de la media del total de valores medidos en una hora determinada para un nodo determinado
################################################################################################################
def extract_mean(IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE):
    filter = df[(df['iid'] == IID_SAMPLE) & (df['H'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
    df2 = pd.DataFrame() #df de almacenamiento
 
    for feature in tqdm(X_features, desc=f'Procesando IID {IID_SAMPLE}'):
        if feature == 'iid':
            df2[feature] = IID_SAMPLE
        else:
            df2[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return df2  
  

################################################################################################################
#función de cálculo de la media del total de valores de Pavg en un período de tiempo 
################################################################################################################
""" def Pavg_mean(IID_SAMPLE, DATETIME_SAMPLE):
    filter_id = df[df['iid'] == IID_SAMPLE] #filtro parámetros input
    df2 = pd.DataFrame() #df de almacenamiento
 
    for feature in tqdm(X_features, desc=f'Procesando IID {IID_SAMPLE}'):
        if feature == 'iid':
            df2[feature] = IID_SAMPLE
        else:
            df2[feature] = [filter_id[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return df   """




iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
print(iid_array) 

""" extraction = [extract_mean(iid, HOUR_SAMPLE, DATETIME_SAMPLE) for iid in iid_array] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
new_df.to_csv('OUT.csv', index=False)  """


filter_id = df[df['iid'] == 2] 
print(filter_id)


plt.figure(figsize=(10, 6))
plt.plot(filter_id['tmstp'], filter_id['Pavg'], linestyle='-', marker='o')
plt.title('Variación de Pavg a lo largo del tiempo')
plt.xlabel('Fecha y Hora')
plt.ylabel('Pavg')
plt.grid(True)
plt.show()

#media = Pavg_mean(42, DATETIME_SAMPLE)
#print(media)
=======
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
>>>>>>> 6d81ec0832753a6b3715246b66df7e7fb3c97c84
