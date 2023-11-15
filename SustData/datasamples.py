import pandas as pd
import numpy as np
import glob as gl
from tqdm import tqdm
import matplotlib.pyplot as plt


path = gl.glob('dataset/preprocessed/new_power_samples_d4*.csv') #power_samples -> OUT.csv
#path2 = gl.glob('NO/power_events/power_events_d2*.csv') #power_events -> OUT2.csv

dfs = [pd.read_csv(file, low_memory=False) for file in path] #lectura de todos los .csv
df = pd.concat(dfs, ignore_index=True) #df con todos los dfs

#parseo de timestamp y creación de nueva columna H
df['tmstp'] = pd.to_datetime(df['tmstp'])
df['H'] = df['tmstp'].dt.strftime('%H') #nueva columna de hora
df['H'] = df['H'].astype(int)

#extracción de features
#X = df.iloc[:, 3:18] #names + values
#X = df.iloc[:, 3:4] #if power_events 
X = df.iloc[:, 11:12]                          #SIMPLIFICACION PARA COGER SOLO Pavg 
X_features = X.columns.to_list() #names to list
X_features.append('iid')
X_features.append('tmstp')


################################################################################################################
#función de cálculo de la media del total de valores medidos en una hora determinada para un nodo determinado
################################################################################################################
def extract_mean(IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE):
    filter = df[(df['iid'] == IID_SAMPLE) & (df['H'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
    df2 = pd.DataFrame() #df de almacenamiento
 
    for feature in tqdm(X_features, desc=f'Procesando IID {IID_SAMPLE} {DATETIME_SAMPLE} {HOUR_SAMPLE}'):
        if feature == 'iid':
            df2[feature] = IID_SAMPLE
        elif feature == 'tmstp':
            df2[feature] = DATETIME_SAMPLE
        else:
            df2[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 

    return df2  
  

################################################################################################################
#DATETIME_SAMPLE = '2011-07-01' #d2
#DATETIME_SAMPLE = '2013-01-01' #d3
DATETIME_SAMPLE = '2014-01-01' #d4
HOUR_SAMPLE = 0

iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
print(iid_array) 
datetime_array = df['datetime'].unique() 
hour_array = df['H'].unique().sort
################################################################################################################


#(PRIMERA EXTRACCIÓN) extracción de media de valores de una hora determinada y fecha determinada para todos los ids (mismo instante temporal)
""" extraction = [extract_mean(iid, HOUR_SAMPLE, DATETIME_SAMPLE) for iid in iid_array] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
new_df.to_csv('OUT.csv', index=False)  """


#extracción de media de valores de la hora 0 para todas las fechas del id 42 
""" extraction = [extract_mean(42, HOUR_SAMPLE, datetime) for datetime in datetime_array] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas


filter_id = df[(df['iid'] == 42)]
plt.figure(figsize=(10, 6))
plt.plot(filter_id['tmstp'], filter_id['Pavg'], linestyle='-')
plt.title('Variación de Pavg a lo largo del tiempo')
plt.xlabel('Fecha y Hora')
plt.ylabel('Pavg')
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(new_df['tmstp'], new_df['Pavg'], linestyle='-')
plt.title('Variación de Pavg a lo largo del tiempo')
plt.xlabel('Timestamp')
plt.ylabel('Pavg')
plt.grid(True)
for n, label in enumerate(plt.gca().xaxis.get_ticklabels()):
    if n % 20 != 0:
        label.set_visible(False)
plt.show() """


#extracción de media de valores de cada hora para todas las fechas del id 42 
extraction = [extract_mean(42, hour, datetime) for datetime in datetime_array for hour in hour_array] 
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
new_df.to_csv('OUT_42_all.csv', index=False) 

plt.figure(figsize=(10, 6))
plt.plot(new_df['tmstp'], new_df['Pavg'], linestyle='-')
plt.title('Variación de Pavg a lo largo del tiempo')
plt.xlabel('Timestamp')
plt.ylabel('Pavg')
plt.grid(True)
for n, label in enumerate(plt.gca().xaxis.get_ticklabels()):
    if n % 25 != 0:
        label.set_visible(False)
plt.show() 


#visualización de todos los valores para todas las fechas del id 42, MUCHAS MUESTRAS -> reducir y hacer medias por día

