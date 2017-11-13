#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arseferreira@gmail.com)      ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  4/8/2015                                          ###
#                                                            ###
# ##############################################################
'''
from bd import engine


class Dao(object):
    '''
    classdocs
    '''

    def __init__(self, T):
        '''
        Constructor
        :param T: clase de la entidad a ser gestionada.
        '''
        self.session = engine.getSession()
        self.T = T

    def add(self, entity):
        '''
        Función que persiste un Objeto a la Base de Datos.
        :param entity: cualquiera de las clases mapeadas a la Base de Datos
        :return: entity
        '''
        self.session.add(entity)
        self.session.commit()
        return entity

    def add_all(self, list_entities):
        '''
        Función que persiste una lista de Objetos a la Base de Datos.
        :param list_entities: cualquiera de las clases mapeadas a la
        Base de Datos.
        :return: list_entities
        '''
        self.session.add_all(list_entities)
        self.session.commit()
        return list_entities

    def delete(self, entity):
        '''
        Función que remueve uno o varios Objetos de la Base de Datos.

        :param entity: cualquiera de las clases mapeadas a la Base de Datos
        '''
        self.session.delete(entity)
        self.session.commit()

    def update(self, entity):
        '''
        Función que actualiza el registro asociado al objeto en la
        Base de datos.
        :param entity: entidad a ser actualizada.
        '''
        self.session.add(entity)
        self.session.commit()
        return entity

    def get_all(self, T):
        '''
        Función que retorna todos los registros para la entidad asociada.
        '''
        return self.session.query(T).all()

    def get(self, id_):
        '''
        Método que recupera una entidad de la base de datos por medio de su id.
        :param id_: id de la entidad a ser recuperada.
        '''
        return self.session.query(self.T).get(id_)
