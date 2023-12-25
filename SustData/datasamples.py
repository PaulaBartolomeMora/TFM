import pandas as pd 
import numpy as np
import glob as gl 
from tqdm import tqdm
import matplotlib.pyplot as plt
from threading import Thread
import time

files_cons = "unzipped/new_power_samples_d2*.csv"
files_prod = "unzipped/env+prod.csv"
files_events = "dataset/no/power_events/power_events*.csv"

iid_prueba = range(1, 24)

# DATETIME_SAMPLE = '2011-07-01' #d2
# DATETIME_SAMPLE = '2013-01-01' #d3
# DATETIME_SAMPLE = '2014-01-01' #d4
# HOUR_SAMPLE = 13
# IID_SAMPLE = 42

threads = []
results = []


################################################################################################################
# función de read files y def features, devuelve el dataframe
################################################################################################################
def read_files(files):
    path = gl.glob(files)
    dfs = []  

    for file in path:
        dfs.append(pd.read_csv(file, low_memory=False))
        print("Leyendo " + file)

    df = pd.concat(dfs, ignore_index=True)  # df con todos los dfs

    # parseo de timestamp y creación de nueva columna H
    df["tmstp"] = pd.to_datetime(df["tmstp"])
    df["h"] = df["tmstp"].dt.strftime("%H")  # nueva columna de hora
    df["h"] = df["h"].astype(int)

    # extracción de features
    if files.startswith(files_cons):
        X = df.iloc[:, 11:12]  # SIMPLIFICACION PARA COGER SOLO Pavg
        iid_array = df["iid"].unique()  # ids nodos que aparecen en el dataset
        # X = df.iloc[:, 3:18] #names + value
    elif files.startswith(files_events):
        X = df.iloc[:, 3:4]
        iid_array = df["iid"].unique()  # ids nodos que aparecen en el dataset
    elif files == files_prod:
        X = df.iloc[:, 16:17]
        iid_array = 0

    X_features = X.columns.to_list()  # names to list
    X_features.append("iid")
    X_features.append("datetime")
    X_features.append("h")
    datetime_array = df["datetime"].unique()
    return df, X_features, iid_array, datetime_array


################################################################################################################
# función de cálculo de la media del total de valores medidos en una hora determinada para un nodo determinado
################################################################################################################
def extract_mean(df, IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE, X_features):
    if (
        IID_SAMPLE == 0
    ):  # se pasa parámetro iid nulo para indicar que no existe columna iid
        filter = df[(df["h"] == HOUR_SAMPLE) & (df["datetime"] == DATETIME_SAMPLE)]
        desc = f"Procesando producción {DATETIME_SAMPLE} {HOUR_SAMPLE}"
    else:
        filter = df[
            (df["iid"] == IID_SAMPLE)
            & (df["h"] == HOUR_SAMPLE)
            & (df["datetime"] == DATETIME_SAMPLE)
        ]  # filtro parámetros input
        desc = f"Procesando consumo de IID {IID_SAMPLE} {DATETIME_SAMPLE} {HOUR_SAMPLE}"

    df2 = pd.DataFrame()  # df de almacenamiento

    for feature in tqdm(X_features, desc):
        if feature == "iid":
            df2[feature] = IID_SAMPLE
        elif feature == "datetime":
            df2[feature] = DATETIME_SAMPLE
        # elif feature == 'h':
        #     df2[feature] == HOUR_SAMPLE
        else:
            df2[feature] = [
                filter[feature].mean()
            ]  # se almacena la media de todas las features según los parámetros input dados
    return df2


################################################################################################################
# función de plot de valores Pavg de un nodo
################################################################################################################
def plot_figure(df, IID_SAMPLE, plotting):
    plt.figure(figsize=(10, 6))

    if plotting == 1:  # production
        plt.plot(df["datetime"], df["solar"], linestyle="-")
        plt.title(f"Solar Energy (MWh)")
        plt.xlabel("Timestamp")
        plt.ylabel("Pavg")
    else:  # consumption
        plt.plot(df["datetime"], df["Pavg"], linestyle="-")
        plt.title(f"Pavg (W) (IID: {IID_SAMPLE})")
        plt.xlabel("Timestamp")
        plt.ylabel("Pavg")
    plt.grid(True)
    for n, label in enumerate(plt.gca().xaxis.get_ticklabels()):
        if n % 25 != 0:
            label.set_visible(False)
    plt.show()


################################################################################################################
# función threading
################################################################################################################
def thread_processing(IID_SAMPLE):
    extraction = [
        extract_mean(df_power_samples, IID_SAMPLE, hour, datetime, X_ps)
        for datetime in datetime_array_ps
        for hour in range(24)
    ]
    result = pd.concat(extraction, ignore_index=True)
    return result


################################################################################################################
################################################################################################################
################################################################################################################


df_power_samples, X_ps, iid_array_ps, datetime_array_ps = read_files(files_cons)
# df_prod, X_pr, iid_array_pr, datetime_array_pr = read_files(files_prod)
# df_power_events = read_files(files_events) #power_events

threads = [
    Thread(target=lambda iid=iid: results.append(thread_processing(iid)), args=())
    for iid in iid_prueba
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# print(results)

for i, result in enumerate(results):
    result.to_csv(f"results/consum_{iid_prueba[i]}.csv", index=False)
