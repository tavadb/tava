#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)      ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  31/8/2016                                          ###
#                                                            ###
# ##############################################################
'''

from datetime import date

from bd.entity import View, ViewResult
from models.dao import Dao


class ViewM(Dao):
    '''
    classdocs
    '''

    def __init__(self):
        super(ViewM, self).__init__(View)

    def add(self, view):

        view.creation = date.today()
        view.update = date.today()
        view.wiht_grid = True
        view.wiht_legend = True
        view.wiht_xvline = True
        view.columns_axis = 1
        return super(ViewM, self).add(view)

    def add_all(self, views):
        _views = []
        for v in views:
            v.creation = date.today()
            v.update = date.today()
            v.wiht_grid = True
            v.wiht_legend = True
            v.wiht_xvline = True
            v.columns_axis = 1
            _views.append(v)
        return super(ViewM, self).add_all(_views)


class ViewResultM(Dao):
    '''
    classdocs
    '''
    def __init__(self):
        super(ViewResultM, self).__init__(View)

    def count_results(self, result_id):
        query = self.session.query(ViewResult).filter_by(result_id=result_id)
        return query.count()

    def use_in_viste(self, result_id):
        return True if self.count_results(result_id) > 0 else False
