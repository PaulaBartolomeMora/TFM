#!/usr/bin/python3


class HLMAC(object):
    """
        Clase para gestionar las HLMACs asignadas
    """

    def __init__(self, hlmac_parent_addr, name, dependency):
        """
            Constructor de la clase HLMAC 
        """
        [self.hlmac, self.depends_on] = HLMAC.hlmac_assign_address(hlmac_parent_addr, name, dependency)
        self.used = False
        self.active = False

    def getOrigin(self):
        """
            Funcion para conseguir el origen de la HLMAC
        """
        return self.hlmac[-1]

    def getNextHop(self):
        """
            Funcion para conseguir el siguiente salto de la HLMAC
        """
        ret_val = None
        if len(self.hlmac) > 1:
            ret_val = self.hlmac[-2]
        return ret_val

    @staticmethod
    def hlmac_assign_address(hlmac_parent_addr, name, dependency):
        """
            Método para asignar una HLMAC a partir de una addr padre
        """
        new_addr = list()
        new_dependence = list()

        if hlmac_parent_addr is not None:
            # No podemos asignar sin más la lista ya que si no se coparten referencias, y serían mutables entre ellas.
            # Por ello, hay que llamar a copy()
            new_addr = hlmac_parent_addr.hlmac.copy()
            new_dependence = hlmac_parent_addr.depends_on.copy()

        # En caso de que haya una dependencia, la añadimos, si no, unicamente heredamos la de los padres
        if dependency is not None:
            new_dependence.append(dependency)

        new_addr.append(name)

        return [new_addr, new_dependence]

    @staticmethod
    def hlmac_cmp_address(hlmac_a, hlmac_b):
        """
            Funcion para comparar dos addr HLMAC
        """
        return hlmac_a.hlmac == hlmac_b.hlmac

    @staticmethod
    def hlmac_check_loop(hlmac_a, name):
        """
            Función para detectar bucles en una HLMAC a asignar 
        """
        return name in hlmac_a.hlmac

    @staticmethod
    def hlmac_addr_print(addr):
        """
            Funcion para imprimir una HLMAC
        """
        return '.'.join(map(str, addr.hlmac))
    
    #############################################################################################
    @staticmethod
    def hlmac_get_addr(addr):
        """
            Funcion para imprimir una HLMAC
        """
        return addr.hlmac
    #############################################################################################

    @staticmethod
    def hlmac_deps_print(deps):
        """
            Funcion para imprimir las deps de una  HLMAC
        """
        ret_str = ''

        if len(deps.depends_on) == 0:
            ret_str = '-'
        else:
            ret_str = str(deps.depends_on)

        return ret_str
