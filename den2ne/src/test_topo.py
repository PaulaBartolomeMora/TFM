#!/usr/bin/python3
from graph.graph import Graph
from den2ne.den2neALG import Den2ne
import dataCollector.brite_intf as BRITE_interface
from dataCollector.dataCollector import DataGatherer
import sys
import time
import os
from datetime import datetime
import csv

#Variables globales
LOSSES = [False, True, False, True]
CAPACITY = [False, False, True, True]
DEBUG_PLOT = False

def prueba(path_results, path_topology, topo_seed, criterion, conf_losses, load_limit, n_runs, path_simtests, sim_file, path_datasets):

    """
    Obj: Realizar las pruebas sistemáticas y guardar los resultados en un fichero de texto.
    ### PARÁMETROS ###
    - path_results (path)   -> Path del directorio en el que se almacenarán los resultados (empezado por ./) Ejemplo: ./results
    - path_topology (path)  -> Path del directorio donde se encuentran los ficheros de la topología en especifico (empieza por ./) Ejemplo: ./data/topos/waxman-30-4/seed_5/
    - topo_seed (int[1,10]) -> Semilla de la topología. Va implícita en path_topology pero para evitar buscar (Tienen que coincidir) Ejemplo: 5 (por seed_5)
    - criterion (int[0,4])  -> Índice del criterio elegido de la lista de criterios que se encuentra en ./den2ne/den2neALG.py
    - conf_losses (int[0,3])-> Índice de elección del escenario de pérdidas. Modifica valores de withLosses y withCap. 4 posibles escenarios
    - load_limit (int[0,1]) -> Existencia o no de límite de carga: (Si=1-No=0)
    - n_runs (int)          -> Número de ejecuciones que servirán para fijar la semilla de ejecución
    ##################
    """

    #Obtención ficheros de la topología
    node_file = path_topology + 'Nodos.csv'
    if not os.path.exists(node_file):
        print('Error, no existe el fichero ' + str(node_file))
        return
    edge_file = path_topology + 'Enlaces.csv'
    if not os.path.exists(edge_file):
        print('Error, no existe el fichero ' + str(edge_file))
        return

    #Crear directorios de resultados si no existen
    if not os.path.isdir(path_results):   #./results
        os.mkdir(path_results)

    data=path_topology.split('/')   #Obtención nombre topologia
    path_results=path_results+'/'+data[3]
    if not os.path.isdir(path_results):  #./results/topo_x_y
        os.mkdir(path_results)
        
        
        
    #############################################################################################
    loads_conf = DataGatherer.getLoads_Config(path_simtests + sim_file) #se pasan desde .sh
    
    dtime = sim_file[sim_file.find('_') + 1:] #se coge el datetime del fichero de pruebas
    dtime = os.path.splitext(dtime)[0]
    #############################################################################################


    #Preparación de fichero de resultados
    file_name='outdata_seed_%d_c_%d_t_%s.csv' % (topo_seed,criterion,dtime) ##
    print('[' + datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + '][INFO] Fichero de resultados generado: ' + path_results + '/' + file_name)  #./results/topo_x_y/outdata_seed_%d_c_%s.csv
    file=open(path_results+ '/' + file_name, 'w')

    n_nodes = int(node_file.split('-')[-2])
    
    
    
    
    #EJECUCIONES = n_runs con semillas
    for seed_run in range(n_runs):
        seed = n_nodes*100 + topo_seed*10 + seed_run
        #Recogemos los datos de la topología BRITE con semilla de ejecución (seed run)
        if load_limit:
            #############################################################################################
            loads = BRITE_interface.cargas_con_limite(node_file, loads_conf, seed) #loads = BRITE_interface.cargas_aleatorias_con_limite(node_file, seed)
            #############################################################################################
        else:
            #############################################################################################
            loads = BRITE_interface.cargas(node_file, loads_conf, seed) #loads = BRITE_interface.cargas_aleatorias(node_file, seed)
            #############################################################################################
        
        edges_conf = DataGatherer.getEdges_Config('data/links_config.csv')
        edges = BRITE_interface.BRITEedges(edge_file, edges_conf, seed)
        positions = BRITE_interface.BRITEpositions(node_file)
        root = BRITE_interface.selectRoot(node_file, seed)

        #Creamos el grafos
        G = Graph(0, loads, edges, list(), edges_conf, None, root) #no se introducen switches (None)

        #ALGORITMO
        G_den2ne_alg = Den2ne(G)

        inicio_id = time.time()
        G_den2ne_alg.spread_ids()
        fin_id = time.time()

        #Ahora seleccionamos las IDS por el criterio
        G_den2ne_alg.selectBestIDs(criterion)
 
        inicio_balance = time.time()
        #############################################################################################
        #losses y capacity -> conf_losses tipo 3
        [total_balance_ideal, abs_flux, data_topo] = G_den2ne_alg.globalBalance(withLosses=LOSSES[conf_losses], withCap=CAPACITY[conf_losses], withDebugPlot=DEBUG_PLOT, positions=positions, path=path_results)
        #############################################################################################
        fin_balance = time.time()
        
        tiempo_balance = fin_balance - inicio_balance
        tiempo_id = fin_id - inicio_id        
        
        #Escritura de resultados
        #FORMATO: seed_run, balance, abs_flux, time_ID, time_balance
        file.write(str(seed) + ',' + str(total_balance_ideal) + ',' + str(abs_flux) + ',' + str(tiempo_id) + ',' + str(tiempo_balance) + '\n')
    
    file.close()
    
    
    
    #############################################################################################   
    dtime_obj = datetime.strptime(dtime, "%Y-%m-%d_%H") #se extraen los valores del datetime    
    dtime_obj = dtime_obj.strftime("%Y-%m-%d %H:%M:%S") #se establece el nuevo formato datetime
    
    modelo = os.path.basename(path_datasets).split('-')[0]
    degree = os.path.basename(path_datasets).split('-')[-1]
    
    file_name2='dataset_seed_%d_cr_%d_t_%s_dg_%s_m_%s.csv' % (topo_seed,criterion,dtime,degree,modelo) ##
    
    # Crear directorios de datasets si no existen
    if not os.path.exists(path_datasets):
        os.makedirs(path_datasets)
    
    with open(path_datasets + '/' + file_name2, 'w', newline='') as file2:
        fieldnames = ['datetime'] + list(data_topo[0].keys()) + ['modelo'] + ['criterion'] + ['degree'] + ['total_balance'] + ['abs_flux']
        writer = csv.DictWriter(file2, fieldnames=fieldnames)
        writer.writeheader()

        for fila in data_topo.values():
            fila['datetime'] = dtime_obj
            fila['modelo'] = modelo
            fila['criterion'] = criterion
            fila['degree'] = degree
            fila['total_balance'] = total_balance_ideal
            fila['abs_flux'] = abs_flux
            writer.writerow(fila)

    #############################################################################################


    

if __name__ == "__main__":
    if (len(sys.argv))!=11:
        print('Error, debe introducir: path de los resultados, path de la topología, semilla, criterio, escenario de pérdidas, límite de carga y número ejecuciones')
        print('AYUDA: resultados (path), topología (path), semilla (int[1-10]), criterio (int[0-4]), perdidas (int[0-3]), límite de carga (int[No=0 o Sí=1]), número ejecuciones (int), tests (path), tests (file), datasets (path)')
        exit(1)
    prueba(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), sys.argv[8], sys.argv[9], sys.argv[10])