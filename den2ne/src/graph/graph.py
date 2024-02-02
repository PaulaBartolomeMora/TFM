#!/usr/bin/python3

from networkx.generators.directed import gn_graph
from .node import Node
from .link import Link
import networkx as nx
import matplotlib.pyplot as plt
import json

class Graph(object):
    """
        Clase para gestionar el gráfo que representará la red de distribución eléctrica
    """

    def __init__(self, delta, loads, edges, switches, edges_conf, json_path=None, root='150'):
        """
            Constructor de la clase Graph el cual conformará el grafo a partir de los datos procesados.
        """
        self.nodes = dict()
        self.root = root
        self.sw_config = self.buildSwitchConfig(switches)
        self.json_path = json_path
        if self.json_path == None:
            self.buildGraph(delta, loads, edges, switches, edges_conf)
        else:
            self.load_json()

    def buildGraph(self, delta, loads, edges, switches, edges_conf):
        """
            Función para generar el grafo
        """

        # Primero vamos a añadir todos los nodos normales del grafo, ya que los tenemos listados con sus cargas en loads.
        for node in loads:
            #self.nodes[node] = Node(node, Node.NORMAL, loads[node][delta])
            #############################################################################################
            self.nodes[node] = Node(node, Node.NORMAL, loads[node][0]["id"], loads[node][0]["load"])
            #############################################################################################

        # Acto seguido vamos añadir todos los nodos virtuales
        for edge in edges:
            if edge["node_a"] not in self.nodes:
                self.nodes[edge["node_a"]] = Node(edge["node_a"], Node.VIRTUAL, 0)
            elif edge["node_b"] not in self.nodes:
                self.nodes[edge["node_b"]] = Node(edge["node_b"], Node.VIRTUAL, 0)

        for sw_edge in switches:
            if sw_edge["node_a"] not in self.nodes:
                self.nodes[sw_edge["node_a"]] = Node(sw_edge["node_a"], Node.VIRTUAL, 0)
            elif sw_edge["node_b"] not in self.nodes:
                self.nodes[sw_edge["node_b"]] = Node(sw_edge["node_b"], Node.VIRTUAL, 0)

        # A continuación, vamos a añadir a los nodos sus vecinos. Cada enlace es bi-direccional.
        for edge in edges:
            self.nodes[edge["node_a"]].addNeighbor(edge["node_b"], Link.NORMAL, 'closed', edge["dist"], edge["conf"], edges_conf[edge["conf"]]["coef_r"], edges_conf[edge["conf"]]["i_max"])
            self.nodes[edge["node_b"]].addNeighbor(edge["node_a"], Link.NORMAL, 'closed', edge["dist"], edge["conf"], edges_conf[edge["conf"]]["coef_r"], edges_conf[edge["conf"]]["i_max"])

        for sw_edge in switches:
            self.nodes[sw_edge["node_a"]].addNeighbor(sw_edge["node_b"], Link.SWITCH, sw_edge["state"], 0, 0, 0, 0)
            self.nodes[sw_edge["node_b"]].addNeighbor(sw_edge["node_a"], Link.SWITCH, sw_edge["state"], 0, 0, 0, 0)




    def buildSwitchConfig(self, switch):
        """
            Función para procesar la configuración inicial de los enlaces switch
        """

        # Nos creamos una variable auxiliar a devolver
        sw_config = dict()

        for sw_links in switch:
            sw_config[switch.index(sw_links)] = sw_links
            sw_config[switch.index(sw_links)]["pruned"] = False

        return sw_config

    def findSwitchID(self, name):
        """
            Función para buscar el index del enlace Switch dado el nombre de alguno de sus extremos
        """
        index = None

        for key in self.sw_config:
            if self.sw_config[key]['node_a'] == name or self.sw_config[key]['node_b'] == name:
                index = key
                break

        return index

    def getSwitchConfig(self, id):
        """
            Función para obtener el estado de un switch
        """
        return self.sw_config[id]['state']

    def setSwitchConfig(self, id, state, pruned=None):
        """
            Función para establecer el estado de un enlace de tipo switch 
        """

        # Primero vamos a modificarlo en el dict que tenemos en la clase del grafo
        self.sw_config[id]['state'] = state

        # Si se debe a una poda
        if pruned is not None:
            self.sw_config[id]['pruned'] = True

        # Acto seguido, debemos buscar los dos nodos que conforman el enlace y modificar sus Objs links para
        # que la info de estado siga siendo coherente.

        # Node A
        self.nodes[self.sw_config[id]['node_a']].links[self.nodes[self.sw_config[id]['node_a']].neighbors.index(self.sw_config[id]['node_b'])].state = state

        # Node B
        self.nodes[self.sw_config[id]['node_b']].links[self.nodes[self.sw_config[id]['node_b']].neighbors.index(self.sw_config[id]['node_a'])].state = state

        # Estos dos ultimos dos pasos si se va a eleiminar posteriormente uno de los nodos
        # va da igual, ya que el obj link se va a eliminar.. Pero de esta forma, hacemos que el metodo
        # sea robusto ante cualquier tipo de interacción



    def setLinkDirection(self, node_a, node_b, direction):
        """
            Funcion para establecer la dirección de un enlace, es decir, hacia donde irá el flujo de potencia
        """

        # Si la dirección es "up", la potencia va de node_b al node_a

        # Si por el contrario, la dirección es "down", la potencia va de node_a al node_b

        # Node A
        self.nodes[node_a].links[self.nodes[node_a].neighbors.index(node_b)].direction = direction

    def getLinkCapacity(self, node_a, node_b):
        """
            Función para obtener la capacidad del enlace conformado por node_a y node_b 
        """
        ret_cap = None

        # Vamos al nodo A, y miramos el enlace con el vecino node_b

        # Si el enlace es de tipo switch.. no hay capacidad
        if self.nodes[node_a].links[self.nodes[node_a].neighbors.index(node_b)].type == Link.NORMAL:
            ret_cap = self.nodes[node_a].links[self.nodes[node_a].neighbors.index(node_b)].capacity

        return ret_cap
    
    
    
    #############################################################################################
    def getLinkDist(self, node_a, node_b):
        """
            Función para obtener la capacidad del enlace conformado por node_a y node_b 
        """
        ret_dist = None

        # Vamos al nodo A, y miramos el enlace con el vecino node_b

        # Si el enlace es de tipo switch.. no hay capacidad
        if self.nodes[node_a].links[self.nodes[node_a].neighbors.index(node_b)].type == Link.NORMAL:
            ret_dist = self.nodes[node_a].links[self.nodes[node_a].neighbors.index(node_b)].dist

        return ret_dist
    #############################################################################################
    
    

    def removeNode(self, name):
        """
            Funcion para eliminar un nodo del grafo
        """

        # Primero vamos a los vecinos y eleminimos los enlaces con el
        for neighbor in self.nodes[name].neighbors:
            # Obtenemos el index a eliminar (Es necesario para los enlaces por ser objs, no vale hacer un remove)
            index_del = self.nodes[neighbor].neighbors.index(name)

            # Machacamos el nodo a eliminar como vecino, y con el index, eliminamos el enlace con el.
            self.nodes[neighbor].neighbors.remove(name)
            del self.nodes[neighbor].links[index_del]

        # Por último eliminamos el nodo de la lista del grafo
        self.nodes.pop(name)

    def pruneGraph(self):
        """
            Method to automagically prune the graph and set the default status of pruned Switch links

            Returns:
                list: A list of the IDs of the nodes that have been pruned.
        """

        nodes_to_prune = {
            'sweep_1': [],
            'sweep_2': []
        }

        # First sweep
        for node in self.nodes:
            if (
                self.nodes[node].type == Node.VIRTUAL and
                self.nodes[node].name != self.root and
                len(self.nodes[node].links) == 1 and
                self.nodes[node].links[0].type == Link.SWITCH
            ):
                nodes_to_prune['sweep_1'].append(self.nodes[node].name)

        # Lets open the switch links so that they dont consume anything
        for node in nodes_to_prune['sweep_1']:
            self.setSwitchConfig(self.findSwitchID(node), 'open', 'pruned')

        for node in nodes_to_prune['sweep_1']:
            self.removeNode(node)

        # Second sweep
        for node in self.nodes:
            if (
                self.nodes[node].type == Node.VIRTUAL and
                len(self.nodes[node].links) == 1 and
                self.nodes[node].links[0].type == Link.NORMAL
            ):
                nodes_to_prune['sweep_2'].append(self.nodes[node].name)

        for node in nodes_to_prune['sweep_2']:
            self.removeNode(node)

        return nodes_to_prune['sweep_1'] + nodes_to_prune['sweep_2']

    def plotGraph(self, positions, title):
        """
            Funcion para pintar el grafo
        """
        G_nx = nx.Graph()
        color_map = []

        for node in self.nodes:
            for link in self.nodes[node].links:
                G_nx.add_edge(
                    self.nodes[node].name, self.nodes[node].neighbors[self.nodes[node].links.index(link)], type_link=link.type, status=link.state)

        edge_normal = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.NORMAL]
        edge_switch_open = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'open']
        edge_switch_closed = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'closed']

        pos = nx.spring_layout(G_nx, k=0.2)

        for position in positions:
            pos[position["node"]] = (position["x"], -position["y"])

        for node in G_nx:
            if self.nodes[node].type == Node.NORMAL:
                color_map.append('#19affa')
            else:
                color_map.append('#95e8d6')

        fig = plt.figure()
        nx.draw_networkx_nodes(G_nx, pos, node_color=color_map, node_size=270)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_normal, width=2)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_open, width=2, alpha=0.5, edge_color="g", style="dashed")
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_closed, width=2, alpha=0.5, edge_color="r", style="dashed")
        nx.draw_networkx_labels(G_nx, pos, font_size=10, font_family="sans-serif")

        plt.axis("off")
        plt.title(title)
        plt.plot()

    def plotDiGraph(self, positions, title):
        """
            Funcion para pintar el grafo dirigido
        """
        G_nx = nx.Graph()
        G_nx = G_nx.to_directed()

        color_map = []

        for node in self.nodes:
            for link in self.nodes[node].links:
                G_nx.add_edge(
                    self.nodes[node].name, self.nodes[node].neighbors[self.nodes[node].links.index(link)], type_link=link.type, status=link.state, direction=link.direction)

        edge_normal = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.NORMAL and d["direction"] == 'up']
        edge_switch_open = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'open' and d["direction"] == 'up']
        edge_switch_closed = [(u, v) for (u, v, d) in G_nx.edges(data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'closed' and d["direction"] == 'up']

        pos = nx.spring_layout(G_nx, k=0.2)

        for position in positions:
            pos[position["node"]] = (position["x"], -position["y"])

        for node in G_nx:
            if self.nodes[node].type == Node.NORMAL:
                color_map.append('#19affa')
            else:
                color_map.append('#95e8d6')

        fig = plt.figure(figsize=(16.0, 10.0))
        nx.draw_networkx_nodes(G_nx, pos, node_color=color_map, node_size=270)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_normal, width=2)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_open, width=2, alpha=0.7, edge_color="g", style="dashed")
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_closed, width=2, alpha=0.7,  edge_color="r", style="dashed")
        nx.draw_networkx_labels(G_nx, pos, font_size=10, font_family="sans-serif")

        plt.axis("off")
        plt.title(title)
        plt.plot()

    def plotStepDiGraph(self, path, positions, title):
        """
            Funcion para pintar el grafo dirigido en pasos
        """
        G_nx = nx.Graph()
        G_nx = G_nx.to_directed()

        color_map = []

        for node in self.nodes:
            for link in self.nodes[node].links:
                G_nx.add_edge(
                    self.nodes[node].name, self.nodes[node].neighbors[self.nodes[node].links.index(link)], type_link=link.type, status=link.state, direction=link.direction)

        edge_normal = [(u, v) for (u, v, d) in G_nx.edges(
            data=True) if d["type_link"] == Link.NORMAL and d["direction"] == 'up']
        edge_switch_open = [(u, v) for (u, v, d) in G_nx.edges(
            data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'open' and d["direction"] == 'up']
        edge_switch_closed = [(u, v) for (u, v, d) in G_nx.edges(
            data=True) if d["type_link"] == Link.SWITCH and d["status"] == 'closed' and d["direction"] == 'up']

        pos = nx.spring_layout(G_nx, k=0.2)

        for position in positions:
            pos[position["node"]] = (position["x"], -position["y"])

        for node in G_nx:
            if self.nodes[node].type == Node.NORMAL:
                color_map.append('#19affa')
            else:
                color_map.append('#95e8d6')

        fig = plt.figure(figsize=(16.0, 10.0))
        nx.draw_networkx_nodes(G_nx, pos, node_color=color_map, node_size=270)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_normal, width=2)
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_open,
                               width=2, alpha=0.7, edge_color="g", style="dashed")
        nx.draw_networkx_edges(G_nx, pos, edgelist=edge_switch_closed,
                               width=2, alpha=0.7,  edge_color="r", style="dashed")
        nx.draw_networkx_labels(G_nx, pos, font_size=10,
                                font_family="sans-serif")

        plt.axis("off")
        plt.title(title)
        plt.plot()
        plt.savefig(path + title + '.png', dpi=100)
        plt.close(fig)

    @staticmethod
    def showGraph():
        """
            Función para representar las figuras generadas, para no bloquear el flujo de ejecución
        """
        # He estado a nada de meterme con threads y subprocesos con la librería de python de multiprocessing..
        # Mejor lo de dejamos así para ahorrar tiempo. Que sea el usuario quien decida cuando bloquear la ejecución..
        plt.show()

    def saveGraph(self, path, json_path = None):#Por ahora el campo json_path es para los test unitarios hasta que se me ocurra otra cosa
        """
            Función para guardar el grafo en un archivo .json
        """
        if json_path == None:
            self.json_path= path
        else:
            self.json_path = json_path
        with open(path, 'w') as file:
             #Primero creo un diccionario que acumule todos los datos que vamos a guardar en el json, y luego lo vamos escribiendo en el json de forma manual
            obj_json = {}
            obj_json['json_path'] = self.json_path
            obj_json['nodes'] = {}
            for n in self.nodes:
                obj_json['nodes'][n]={}
                obj_json['nodes'][n]['name'] = self.nodes[n].name 
                obj_json['nodes'][n]['type'] = self.nodes[n].type
                obj_json['nodes'][n]['load'] = self.nodes[n].load
                obj_json['nodes'][n]['neighbors'] = list(self.nodes[n].neighbors)
                obj_json['nodes'][n]['links'] = list()
                cont=0
                for i in obj_json['nodes'][n]['neighbors']:
                    obj_json['nodes'][n]['links'].append({'node_a': self.nodes[n].links[cont].node_a, 'node_b': self.nodes[n].links[cont].node_b, 'direction': self.nodes[n].links[cont].direction, 'type': self.nodes[n].links[cont].type, 'state': self.nodes[n].links[cont].state, 'dist': self.nodes[n].links[cont].dist, 'conf': self.nodes[n].links[cont].conf, 'coef_R': self.nodes[n].links[cont].coef_R, 'capacity': self.nodes[n].links[cont].capacity})
                    cont+=1
                obj_json['nodes'][n]['ids'] = list()
                cont = 0
                for j in self.nodes[n].ids:
                    obj_json['nodes'][n]['ids'].append({'active': self.nodes[n].ids[cont].active, 'depends_on': self.nodes[n].ids[cont].depends_on, 'hlmac': list(), 'used': self.nodes[n].ids[cont].used})
                    obj_json['nodes'][n]['ids'][cont]['hlmac'] = list(self.nodes[n].ids[cont].hlmac)
                    cont +=1
            obj_json['root'] = self.root
            obj_json['sw_config'] = self.sw_config.copy()

            #Una vez hemos creado obj_json ahora vamos a ir creando el json a mano para así obtenerlo con las tabulaciones que queremos para verlo mucho mejor
            file.write('{\n')
            file.writelines('\t"json_path": "' + str(obj_json['json_path'])+'",\n')
            file.write('\t"nodes": {\n')
            cont1 = 0
            for i in obj_json['nodes']:
                if cont1 != 0: #Uso esto para poner las comas si hay más elementos en el diccionario obj_json['nodes']
                    file.writelines(',\n')
                cont1+=1
                file.writelines('\t\t"'+ str(i) +'": {\n')
                file.writelines('\t\t\t"ids": [\n')
                cont = 0
                for j in obj_json['nodes'][i]['ids']:
                    file.write('\t\t\t\t\t')
                    file.writelines(json.dumps(obj_json['nodes'][i]['ids'][cont]))
                    cont+=1
                    try:
                        if obj_json['nodes'][i]['ids'][cont]:
                            file.write(',\n')
                    except:
                        continue
                file.write('],\n')  
                file.writelines('\t\t\t"links": [\n')
                cont = 0
                for j in obj_json['nodes'][i]['links']:
                    file.writelines('\t\t\t\t\t'+ json.dumps(obj_json['nodes'][i]['links'][cont]))
                    cont+=1
                    try:
                        if obj_json['nodes'][i]['links'][cont]:
                            file.write(',\n')
                    except:
                        continue
                file.write('],\n')  
                file.writelines('\t\t\t"load": ' + str(obj_json['nodes'][i]['load'])+ ',\n')
                file.writelines('\t\t\t"name": ' + obj_json['nodes'][i]['name']+ ',\n')
                file.writelines('\t\t\t"neighbors": ' + json.dumps(obj_json['nodes'][i]['neighbors'])+ ',\n')
                file.writelines('\t\t\t"type": ' + str(obj_json['nodes'][i]['type'])+ '}')
            file.write('\n\t'+'},')
            file.writelines('\t"root": "' + str(obj_json['root']) + '",\n')
            file.writelines('\t"sw_config": {\n')
            for k in obj_json['sw_config']:
                file.writelines('\t\t"'+ str(k) +'": ' + json.dumps(obj_json['sw_config'][k]))
                try:
                    if obj_json['sw_config'][k+1]:
                        file.write(',\n')
                except:
                    file.write('\n')
            file.write('\t}\n')
            file.write('}')


    def load_json(self):
        """
            Función para cargar el grafo desde un json
        """
        path = self.json_path
        with open(path) as file:
            data = json.load(file)
            #Me creo un diccionario auxiliar para acumular todos los valores de los nodos
            #y posteriormente voy creando cada nodo y añadiendo los corresponcientes vecinos
            aux = data['nodes'].copy()
            for i in aux:
                self.nodes[i] = Node(aux[i]['name'], aux[i]['type'], aux[i]['load'])
                cont = 0
                for n in aux[i]['neighbors']:
                    capacidad = aux[i]['links'][cont]['capacity']
                    if capacidad == None:
                        capacidad = 0
                    self.nodes[i].addNeighbor(n, aux[i]['links'][cont]['type'], aux[i]['links'][cont]['state'], aux[i]['links'][cont]['dist'], aux[i]['links'][cont]['conf'], aux[i]['links'][cont]['coef_R'], (capacidad*1000)/Link.VOLTAGE)
                    cont +=1

            self.root = data['root']
            self.sw_config = data['sw_config'].copy()

