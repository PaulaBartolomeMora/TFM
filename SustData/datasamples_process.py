import pandas as pd 
import glob as gl
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Process, Manager

files_cons = "unzipped/new_power_samples_d2*.csv"
files_prod = "unzipped/env+prod.csv"
files_events = "dataset/no/power_events/power_events*.csv"

iid_prueba = range(1, 24)

def read_files(files):
    path = gl.glob(files)
    dfs = []

    for file in path:
        dfs.append(pd.read_csv(file, low_memory=False))
        print("Leyendo " + file)

    df = pd.concat(dfs, ignore_index=True)

    df["tmstp"] = pd.to_datetime(df["tmstp"])
    df["h"] = df["tmstp"].dt.strftime("%H")
    df["h"] = df["h"].astype(int)

    if files.startswith(files_cons):
        X = df.iloc[:, 11:12]
        iid_array = df["iid"].unique()
    elif files.startswith(files_events):
        X = df.iloc[:, 3:4]
        iid_array = df["iid"].unique()
    elif files == files_prod:
        X = df.iloc[:, 16:17]
        iid_array = 0

    X_features = X.columns.to_list()
    X_features.append("iid")
    X_features.append("datetime")
    X_features.append("h")
    datetime_array = df["datetime"].unique()
    return df, X_features, iid_array, datetime_array

def extract_mean(df, IID_SAMPLE, HOUR_SAMPLE, DATETIME_SAMPLE, X_features, result_dict, progress):
    if IID_SAMPLE == 0:
        filter = df[(df["h"] == HOUR_SAMPLE) & (df["datetime"] == DATETIME_SAMPLE)]
        desc = f"Procesando producción {DATETIME_SAMPLE} {HOUR_SAMPLE}"
    else:
        filter = df[
            (df["iid"] == IID_SAMPLE)
            & (df["h"] == HOUR_SAMPLE)
            & (df["datetime"] == DATETIME_SAMPLE)
        ]
        desc = f"Procesando consumo de IID {IID_SAMPLE} {DATETIME_SAMPLE} {HOUR_SAMPLE}"

    df2 = pd.DataFrame()

    for feature in X_features:
        if feature == "iid":
            df2[feature] = IID_SAMPLE
        elif feature == "datetime":
            df2[feature] = DATETIME_SAMPLE
        else:
            df2[feature] = [filter[feature].mean()]

    result_dict[IID_SAMPLE] = df2
    progress.value += 1

def process_data(iid, df_power_samples, datetime_array_ps, X_ps, result_dict, progress):
    extraction = [
        extract_mean(df_power_samples, iid, hour, datetime, X_ps, result_dict, progress)
        for datetime in datetime_array_ps
        for hour in range(24)
    ]

if __name__ == "__main__":
    df_power_samples, X_ps, iid_array_ps, datetime_array_ps = read_files(files_cons)

    manager = Manager()
    result_dict = manager.dict()
    progress = manager.Value('i', 0)

    processes = [
        Process(target=process_data, args=(iid, df_power_samples, datetime_array_ps, X_ps, result_dict, progress))
        for iid in iid_prueba
    ]

    for process in processes:
        process.start()

    total_tasks = len(datetime_array_ps) * len(iid_prueba) * 24
    with tqdm(total=total_tasks, desc="Progreso total del script") as pbar:
        while progress.value < total_tasks:
            pbar.update(progress.value - pbar.n)

    for process in processes:
        process.join()

    for iid, result in result_dict.items():
        result.to_csv(f"results/consum_{iid}.csv", index=False)


