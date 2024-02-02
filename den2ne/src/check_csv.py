#!/usr/bin/python3
import sys
import test_topo

REPORT_PATH = './report.txt'

def revision(csv_path):
    out_data = list()
    with open(csv_path, 'r') as file:
        # Recogemos todas las muestras en la variable data
        data = file.readlines()
        time_reference = float(data[0].split(',')[3]) # Tomamos la medida de tiempos ID que es la columna 3
        time_reference2 = float(data[1].split(',')[3])
        for i in range(len(data)):
            if i == 1:
                if 2*time_reference < time_reference2:
                    out_data.append(data[0])

                elif 2*time_reference2 < time_reference:
                    out_data.append(data[1])
                    time_reference = time_reference2

            next_time = float(data[i].split(',')[3])
            if 2*time_reference > next_time:
                out_data.append(data[i])

            if len(out_data)>= 20:
                break
    #Guardamos las muestras buenas
    with open(csv_path, 'w') as file:
        for i in out_data:
            file.write(i)

if __name__ == "__main__":
    revision(sys.argv[1])
