import random

LIMITE_GLOBAL_CARGA = 250


# def conf_edges_aleatorio(seed):
#     """
#         Función que genera las configuraciones de los enlaces
#     """
#     random.seed(seed)
#     edges_conf = dict()
#     n_conf = random.randint(3, 15)  #Selecciona el numero de configuraciones de enlaces que va a haber
#     for conf in range(n_conf):
#         edges_conf[conf] = dict()
#         edges_conf[conf]['coef_r'] = random.uniform(0, 2.5)
#         edges_conf[conf]['i_max'] = random.randint(40, 200)
#         edges_conf[conf]['section'] = random.randint(0, 100)

#     return edges_conf

def BRITEpositions(node_file):
    """
        Funcion para recolectar las posiciones de los nodos generados por BRITE
    """
    positions = list()

    with open(node_file, "r") as file:
        for datos_lectura in file.readlines():
            positions.append({"node": datos_lectura.split(';')[0], "x": float(datos_lectura.split(';')[1]), "y": float(datos_lectura.split(';')[2])})

    return positions

def BRITEedges(edge_file, edges_conf, seed):
    """
        Funcion para reloectar los enlaces generados por BRITE
        Para asignar una configuración específica a cada enlace le asignamos una aleatoria de la lista conf_edges
    """
    random.seed(seed)
    n_conf = len(list(edges_conf.keys()))
    edges= list()
    with open(edge_file, "r") as file:
        for datos_lectura in file.readlines():
            edges.append({"node_a": datos_lectura.split(';')[0], "node_b": datos_lectura.split(';')[1], "dist": int(datos_lectura.split(';')[2]), "conf": random.randint(1, n_conf)})

    return edges




#############################################################################################

def cargas(node_file, loads_conf, seed):
    """
        Función que introduce las cargas a partir de los perfiles siguiendo una distribución uniforme
    """
    random.seed(seed)
    n_conf = len(list(loads_conf.keys())) #nº de perfiles de carga       
    loads = dict() #cargas a devolver
    n_nodos = int(node_file.split('-')[-2]) #nº de nodos en la topo
    
    for nodo in range(n_nodos):
        loads[str(nodo)] = list()
        select_id = random.randint(1, n_conf) #selección nodo de 1 a 23
        loads[str(nodo)].append({"id": select_id, "load": loads_conf[select_id]["pot_fin"]}) #coge id seleccionado y pot final correspondiente
        #loads[str(nodo)].append(loads_conf[select_id]["pot_fin"])
        
    #print(loads) #####PARA DEPURAR -> ESTO OK
    #print(ids) #####PARA DEPURAR -> ESTO OK
    return loads

#############################################################################################

def cargas_con_limite(node_file, loads_conf, seed):
    """
        Función que introduce las cargas a partir de los perfiles siguiendo una distribución uniforme sin superar la carga global máxima
    """
    random.seed(seed)

    cargas = list() #Variable auxiliar para luego hacer el shuffle
    carga_restante = LIMITE_GLOBAL_CARGA

    n_conf = len(list(loads_conf.keys())) #nº de perfiles de carga         
    loads = dict() #lista final de cargas    
    ids = dict() #ids seleccionados para cada nodo  
    n_nodos = int(node_file.split('-')[-2]) #nº de nodos en la topo
    
    for nodo in range(n_nodos):
        if carga_restante == 0: #Si ya no queda más carga global asignamos 0
            cargas.append(0)
        else:
            select_id = random.randint(1, n_conf)
            carga_individual = loads_conf[select_id]["pot_fin"]
            if carga_restante < abs(carga_individual): #Si lo que queda es menor de lo que ibmaos a signar, asignamos lo que queda
                cargas.append(carga_restante)
                carga_restante = 0
            else: #Si queda suficiente carga
                carga_restante = carga_restante - abs(carga_individual)
                cargas.append(carga_individual)
    
    random.shuffle(cargas) #Mezclamos las cargas para que no se queden todos los 0 al final
    for nodo in range(n_nodos):
        loads[str(nodo)] = list()
        loads[str(nodo)].append({"id": select_id, "load": loads_conf[select_id]["pot_fin"]}) #coge id seleccionado y pot final correspondiente
    return loads

#############################################################################################


# def cargas_aleatorias(node_file, semilla):
#     """
#         Función que genera cargas aleatorias siguiendo una distribución uniforme
#     """
#     random.seed(semilla)
#     loads = dict()
#     n_nodos = int(node_file.split('-')[-2])
#     for nodo in range(n_nodos):
#         loads[str(nodo)] = list()
#         loads[str(nodo)].append(random.uniform(-4, 4))
#     return loads

# def cargas_aleatorias_con_limite(node_file, semilla):
#     """
#         FUnción que genera cargas aleatorias sin superar la carga global máxima
#     """
#     random.seed(semilla)
#     loads = dict()
#     cargas = list() #Variable auxiliar para luego hacer el shuffle
#     carga_restante = LIMITE_GLOBAL_CARGA
#     n_nodos = int(node_file.split('-')[-2])
#     for nodo in range(n_nodos):
#         if carga_restante == 0: #Si ya no queda más carga global asignamos 0
#             cargas.append(0)
#         else:
#             carga_individual = random.uniform(-4, 4)
#             if carga_restante < abs(carga_individual): #Si lo que queda es menor de lo que ibmaos a signar, asignamos lo que queda
#                 cargas.append(carga_restante)
#                 carga_restante = 0
#             else: #Si queda suficiente carga
#                 carga_restante = carga_restante - abs(carga_individual)
#                 cargas.append(carga_individual)
#     random.shuffle(cargas) #Mezclamos las cargas para que no se queden todos los 0 al final
#     for nodo in range(n_nodos):
#         loads[str(nodo)] = list()
#         loads[str(nodo)].append(cargas[nodo])
#     return loads

def selectRoot(node_file, seed):
    """
        Función que selecciona cuál es el root en la topología BRITE
        Lo pongo aquí para usar el módulo random solamente aquí
    """
    random.seed(seed)
    n_nodos = int(node_file.split('-')[-2])
    root = str(random.randint(0, n_nodos - 1))
    return root

# def selectMultiRoot(node_file, n_roots, seed):
#     """
#         Función que selecciona cuales son los root en la topología BRITE
#         Esta función es para el uso de den2neMultiroot
#         Lo pongo aquí para usar el módulo random solamente aquí
#     """
#     random.seed(seed)
#     root = list()
#     n_nodos = int(node_file.split('-')[-2])
#     # Si hay más roots que nodos cerramos la ejecucion
#     if n_roots > n_nodos:
#         print('Error: Está intentando generar una topología con más nodos root que nodos en la topologia.')
#         exit(0)
    
#     while len(root) < n_roots:
#         new_root = str(random.randint(0, n_nodos-1))
#         if new_root not in root:
#             root.append(new_root)
#     return root
