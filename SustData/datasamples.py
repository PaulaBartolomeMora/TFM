import pandas as pd
import numpy as np
import glob as gl
from tqdm import tqdm
import matplotlib.pyplot as plt


################################################################################################################
#función de read files y def features, devuelve el dataframe
################################################################################################################
def read_files(files):
    path = gl.glob(files) 
    dfs = [pd.read_csv(file, low_memory=False) for file in path] #lectura de todos los .csv
    df = pd.concat(dfs, ignore_index=True) #df con todos los dfs

    #parseo de timestamp y creación de nueva columna H
    df['tmstp'] = pd.to_datetime(df['tmstp'])
    df['h'] = df['tmstp'].dt.strftime('%H') #nueva columna de hora
    df['h'] = df['h'].astype(int)

    #extracción de features
    if files == 'dataset/preprocessed/new_power_samples_d4*.csv':
        X = df.iloc[:, 11:12]  #SIMPLIFICACION PARA COGER SOLO Pavg 
        iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
        #X = df.iloc[:, 3:18] #names + value
    elif files == 'NO/power_events/power_events*.csv':
        X = df.iloc[:, 3:4]
        iid_array = df['iid'].unique() #ids nodos que aparecen en el dataset
    elif files == 'dataset/env+prod.csv':
        X = df.iloc[:, 16:17]
        iid_array = 0
   
    X_features = X.columns.to_list() #names to list
    X_features.append('iid')
    X_features.append('datetime')
    X_features.append('h') 
    datetime_array = df['datetime'].unique() 
        
    return df, X_features, iid_array, datetime_array



################################################################################################################
#función de cálculo de la media del total de valores medidos en una hora determinada para un nodo determinado
################################################################################################################
def extract_mean(df, IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE, X_features):
    if IID_SAMPLE == 0: #se pasa parámetro iid nulo para indicar que no existe columna iid
        filter = df[(df['h'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] 
        desc=f'Procesando producción {DATETIME_SAMPLE} {HOUR_SAMPLE}'
    else:
        filter = df[(df['iid'] == IID_SAMPLE) & (df['h'] == HOUR_SAMPLE) & (df['datetime'] == DATETIME_SAMPLE)] #filtro parámetros input
        desc=f'Procesando consumo de IID {IID_SAMPLE} {DATETIME_SAMPLE} {HOUR_SAMPLE}'
    
    df2 = pd.DataFrame() #df de almacenamiento
 
    for feature in tqdm(X_features, desc):
        if feature == 'iid':
            df2[feature] = IID_SAMPLE
        elif feature == 'datetime':
            df2[feature] = DATETIME_SAMPLE
        # elif feature == 'h':
        #     df2[feature] == HOUR_SAMPLE 
        else:
            df2[feature] = [filter[feature].mean()] #se almacena la media de todas las features según los parámetros input dados 
    return df2  
  


################################################################################################################
#función de plot de valores Pavg de un nodo
################################################################################################################
def plot_figure(df, IID_SAMPLE, plotting):
    plt.figure(figsize=(10, 6))
    
    if plotting == 1: #production
        plt.plot(df['datetime'], df['solar'], linestyle='-')
        plt.title(f'Solar Energy (MWh)')
        plt.xlabel('Timestamp')
        plt.ylabel('Pavg')        
    else: #consumition
        plt.plot(df['datetime'], df['Pavg'], linestyle='-')
        plt.title(f'Pavg (W) (IID: {IID_SAMPLE})')
        plt.xlabel('Timestamp')
        plt.ylabel('Pavg')
    plt.grid(True)
    for n, label in enumerate(plt.gca().xaxis.get_ticklabels()):
        if n % 25 != 0:
            label.set_visible(False)
    plt.show() 




#DATETIME_SAMPLE = '2011-07-01' #d2
#DATETIME_SAMPLE = '2013-01-01' #d3
DATETIME_SAMPLE = '2014-01-01' #d4
HOUR_SAMPLE = 13
#IID_SAMPLE = 42


################################################################################################################
################################################################################################################
################################################################################################################



df_power_samples, X_ps, iid_array_ps, datetime_array_ps = read_files('dataset/preprocessed/new_power_samples_d4*.csv') 
df_prod, X_pr, iid_array_pr, datetime_array_pr = read_files('dataset/env+prod.csv') 
#df_power_events = read_files('NO/power_events/power_events_d2*.csv') #power_events 
#print(df_power_samples.head(1))
#print(df_prod.head(1))


#(PRIMERA EXTRACCIÓN) extracción de media de valores de una hora determinada y fecha determinada para todos los ids (mismo instante temporal)
extraction = [extract_mean(df_power_samples, iid, HOUR_SAMPLE, DATETIME_SAMPLE, X_ps) for iid in iid_array_ps] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
new_df.to_csv('OUT.csv', index=False)  


#extracción de media de valores de la hora x para todas las fechas del id 42 
""" extraction = [extract_mean(42, HOUR_SAMPLE, datetime, X_ps) for datetime in datetime_array_ps] #titulos + filas
new_df = pd.concat(extraction, ignore_index=True) #único titulo + filas
plot_figure(new_df, 42)
filter_id = df[(df['iid'] == 42)]
plot_figure(filter_id, 42)"""


#a partir de aquí pruebas##################################################

""" 

IID_SAMPLE = 4
#extracción de media de valores de cada hora para todas las fechas del id 42                                                                              
extraction = [extract_mean(df_power_samples, IID_SAMPLE, hour, datetime, X_ps) for datetime in datetime_array_ps for hour in range(24)] 
df_4 = pd.concat(extraction, ignore_index=True) #único titulo + filas
df_4.to_csv('consum_4.csv', index=False) 
#plot_figure(df_4, IID_SAMPLE)  
#out = pd.read_csv('consum_4.csv')
#plot_figure(out, IID_SAMPLE, 0)


IID_SAMPLE = 9
#extracción de media de valores de cada hora para todas las fechas del id 42                                                                              
extraction = [extract_mean(df_power_samples, IID_SAMPLE, hour, datetime, X_ps) for datetime in datetime_array_ps for hour in range(24)] 
df_9 = pd.concat(extraction, ignore_index=True) #único titulo + filas
df_9.to_csv('consum_9.csv', index=False) 
#plot_figure(df_9, IID_SAMPLE)  
#out = pd.read_csv('consum_9.csv')
#plot_figure(out, IID_SAMPLE, 0)


IID_SAMPLE = 13
#extracción de media de valores de cada hora para todas las fechas del id 42                                                                              
extraction = [extract_mean(df_power_samples, IID_SAMPLE, hour, datetime, X_ps) for datetime in datetime_array_ps for hour in range(24)] 
df_13 = pd.concat(extraction, ignore_index=True) #único titulo + filas
df_13.to_csv('consum_13.csv', index=False) 
#plot_figure(df_13, IID_SAMPLE)  
#out = pd.read_csv('consum_13.csv')
#plot_figure(out, IID_SAMPLE, 0)


IID_SAMPLE = 20
#extracción de media de valores de cada hora para todas las fechas del id 42                                                                              
extraction = [extract_mean(df_power_samples, IID_SAMPLE, hour, datetime, X_ps) for datetime in datetime_array_ps for hour in range(24)] 
df_20 = pd.concat(extraction, ignore_index=True) #único titulo + filas
df_20.to_csv('consum_20.csv', index=False) 
#plot_figure(df_20, IID_SAMPLE)  
#out = pd.read_csv('consum_20.csv')
#plot_figure(out, IID_SAMPLE, 0)


IID_SAMPLE = 25
#extracción de media de valores de cada hora para todas las fechas del id 42                                                                              
extraction = [extract_mean(df_power_samples, IID_SAMPLE, hour, datetime, X_ps) for datetime in datetime_array_ps for hour in range(24)] 
df_25 = pd.concat(extraction, ignore_index=True) #único titulo + filas
df_25.to_csv('consum_25.csv', index=False) 
#plot_figure(df_13, IID_SAMPLE)  
#out = pd.read_csv('consum_13.csv')
#plot_figure(out, IID_SAMPLE, 0)


#obtener media de producción de una hora, comparar con media de consumo de un nodo y operar
mean_production = [extract_mean(df_prod, 0, hour, datetime, X_pr) for datetime in datetime_array_pr for hour in range(24)] 
df_mean_production = pd.concat(mean_production, ignore_index=True) #único titulo + filas
df_mean_production.to_csv('mean_production.csv', index=False)  
#df_mean_production = pd.read_csv('mean_production.csv')
#plot_figure(df_mean_production, 0, 1) 


 """