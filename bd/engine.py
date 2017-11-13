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

# -- motor, que la Sesión utilizará para la conexión recursos
from sqlalchemy import create_engine
import os
_db_path = os.path.join(os.getcwd(), 'tava.db')
engine = create_engine('sqlite:///' + _db_path, echo=True)

# ------------------------------------------------------------
# -- crea o actualiza la base de datos
# ------------------------------------------------------------
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# Base.metadata.create_all(engine)


def createDataDase():
    Base.metadata.create_all(engine)


# ------------------------------------------------------------
# -- crear una clase "Sesión" configurado
# ------------------------------------------------------------
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


def getSession():
    return session
