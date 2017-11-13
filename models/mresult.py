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

from datetime import date

from bd.entity import Result
from models.dao import Dao


class ResultModel(Dao):
    '''
    classdocs
    '''

    def __init__(self):
        super(ResultModel, self).__init__(Result)

    def add(self, result):

        result.creation = date.today()
        result.update = date.today()
        return super(ResultModel, self).add(result)

    def add_all(self, results):
        _results = []
        for r in results:
            r.creation = date.today()
            r.update = date.today()
            _results.append(r)
        return super(ResultModel, self).add_all(_results)

    def update(self, result):
        result.update = date.today()
        return super(ResultModel, self).update(result)

    def update_init(self, result):
        return super(ResultModel, self).update(result)
