#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingeniería en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)     ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  4/8/2015                                          ###
#                                                            ###
# ##############################################################
'''
from datetime import date
from sqlalchemy import or_

from bd.entity import Project as P
from models.dao import Dao


T_OPEN = 1
T_CLOSED = 2
T_HIDDEN = 3


class ProjectM(Dao):

    def __init__(self):
        super(ProjectM, self).__init__(P)

    def add(self, project):
        project.blog = ''
        project.state = T_OPEN
        project.creation = date.today()
        return super(ProjectM, self).add(project)

    def all(self):
        return self.get_all()

    def state_not_hidden(self):
        return self.session.query(P).\
            filter(P.state != T_HIDDEN).order_by(P.state).all()

    def state_open(self):
        return self.session.query(P).\
            filter_by(state=T_OPEN).order_by(P.name).all()

    def state_close(self):
        return self.session.query(P).\
            filter_by(state=T_CLOSED).order_by(P.name).all()

    def state_hidden(self):
        return self.session.query(P).\
            filter_by(state=T_HIDDEN).order_by(P.name).all()

    def names_not_hidden(self):
        tuple_names = self.session.query(P.name).\
            filter(P.state != T_HIDDEN).order_by(P.name).all()
        return [var[0] for var in tuple_names]

    def names_hidden(self):
        tuple_names = self.session.query(P.name).\
            filter_by(state=T_HIDDEN).order_by(P.name).all()
        return [var[0] for var in tuple_names]

    def update_by_open(self, P):
        P.state = T_OPEN
        P.proj_open = True
        return self.update(P)

    def update_by_close(self, P, proj_open, pack_file, pack_view):
        P.state = T_CLOSED
        P.proj_open = proj_open
        P.pack_file = pack_file
        P.pack_view = pack_view
        return self.update(P)

    def update_by_unhide(self, P):
        P.state = T_OPEN
        return self.update(P)

    def update_by_hide(self, P):
        P.state = T_HIDDEN
        P.occultation = date.today()
        return self.update(P)

    def for_unhide(self):
        ret = {}
        for pro in self.state_hidden():
            ret[pro.name] = pro
        return ret

    def get_names_project(self):
        '''
        Método que obtiene todos los nombres de proyectos, en los estados
        OPEN y CLOSED, ordenados por estado.
        '''
        list_names = []

        list_ = self.session.query(P.name).\
            filter(or_(P.state == T_OPEN, P.state == T_CLOSED)).\
            order_by(P.state)
        for name in list_:
            list_names.append(list(name).pop())

        return list_names

    def get_hidden_names_projects(self):
        '''
        Método que obtiene todos los nombres de proyectos en el estado HIDDEN,
        ordenados por nombre.
        '''
        list_names = []
        list_ = self.session.query(P.name).filter_by(state=T_HIDDEN).\
            order_by(P.name).all()
        for name in list_:
            list_names.append(list(name).pop())

        return list_names
