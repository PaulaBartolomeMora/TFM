#!/usr/bin/python3

import csv


class DataGatherer(object):
    """
        Clase para recolectar los datos suministrados en formato CSV
    """

    @staticmethod
    def getLoads(filename, threshold):
        """
            Funcion para recolectar las cargas de los nodos
        """

        loads = dict()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines != 0:
                        loads[row[0]] = [round(float(load), threshold)
                                         for load in row[1:]]
                    lines += 1

        except Exception as e:
            print(str(e))

        return loads

    @staticmethod
    def getEdges(filename):
        """
            Funcion para recolectar los enlaces del grafo
        """

        edges = list()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines >= 3:
                        edges.append(
                            {"node_a": row[0], "node_b": row[1], "dist": int(row[2]), "conf": int(row[3])})
                    lines += 1

        except Exception as e:
            print(str(e))

        return edges

    # @staticmethod
    # def getSwitches(filename):
    #     """
    #         Funcion para recolectar los enlaces especiales del grafo con posibilidad de conmutar
    #     """

    #     switches = list()

    #     try:
    #         with open(filename, 'r') as file:
    #             reader = csv.reader(file)
    #             lines = 0
    #             for row in reader:
    #                 if lines >= 3:
    #                     switches.append(
    #                         {"node_a": row[0], "node_b": row[1], "state": row[2]})
    #                 lines += 1

    #     except Exception as e:
    #         print(str(e))

    #     return switches

    @staticmethod
    def getPositions(filename):
        """
            Funcion para recolectar las posiciones de todos los nodos
        """

        postions = list()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    postions.append({"node": row[0], "x": float(row[1]), "y": float(row[2])})

        except Exception as e:
            print(str(e))

        return postions

    @staticmethod
    def getEdges_Config(filename):
        """
            Funcion para recolectar las configuraciones de los enlaces
        """

        confs = dict()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines != 0:
                        confs[int(row[0])] = {"coef_r": float(row[1]), "i_max": float(row[2]), "section": row[3]}
                    lines += 1

        except Exception as e:
            print(str(e))

        return confs
    
    
    
    
    
    #############################################################################################
    
    @staticmethod
    def getLoads_Config(filename):
        """
            Funcion para recolectar las configuraciones de carga
        """

        confs = dict()

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                lines = 0
                for row in reader:
                    if lines != 0:
                        confs[int(row[0])] = {"pot_prod": float(row[9])/1000, "pot_cons": float(row[10])/1000, "pot_fin": float(row[11])/1000}
                    lines += 1

        except Exception as e:
            print(str(e))

        #print(confs) #####PARA DEPURAR -> ESTO OK
        return confs
    
        #############################################################################################