#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)     ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  13/10/2015                                        ###
#                                                            ###
# ##############################################################
'''

from bd.entity import Iteration
from models.dao import Dao


class IterationModel(Dao):
    '''
    classdocs
    '''

    def __init__(self):
        super(IterationModel, self).__init__(Iteration)

    def add(self, iteration):

        return super(Iteration, self).add(iteration)

    def add_all(self, iterations):
        return super(Iteration, self).add_all(iterations)

    def update(self, iteration):
        return super(Iteration, self).update(iteration)
