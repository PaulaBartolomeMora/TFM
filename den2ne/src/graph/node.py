#!/usr/bin/python3

from den2ne.den2neHLMAC import HLMAC
from .link import Link


class Node(object):
    """
        Clase para gestionar un nodo del grafo
    """

    # Declaramos los tipos de nodos mediante variables estáticas de la clase
    NORMAL = 1
    VIRTUAL = 0

    def __init__(self, name, type_node, id_orig, load=0):
        """
            Constructor de la clase Node
        """
        self.name = name
        self.type = type_node
        self.load = load
        #############################
        self.id_orig = id_orig #id de tipo de nodo del que se ha escogido la carga
        #############################
        self.neighbors = list()
        self.links = list()
        self.ids = list()
        self.ids_root_count = 0  # Lo usamos solamente para den2neMultiroot.

    def addNeighbor(self, neighbor, type_link, state, dist, conf, coef_r, i_max):
        """
            Funcion para añadir un vecino
        """
        self.neighbors.append(neighbor)
        self.links.append(Link(self.name, neighbor, type_link, state, dist, conf, coef_r, i_max))

    def getActiveID(self):
        """
            Función para obtener el ID activo
        """
        ret_ID = None

        for id in self.ids:
            if id.active is True:
                ret_ID = id
                break
        return ret_ID

    def getIndexID(self, id_to_check):
        """
            Funcion para obtener el indexs de una lista de saltos
        """

        # Aqui no vamos a trabajar con los Objs HLMACs, vamos atrabajar directamente con la lista de chars
        
        ret_index = None

        for id in self.ids:
            if id_to_check == id.hlmac:
                ret_index = self.ids.index(id)
                break
            
        return ret_index
