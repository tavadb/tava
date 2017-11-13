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
# Creado:  13/10/2015                                          ###
#                                                            ###
# ##############################################################
'''

import os
DIR_TEMP = ''


def tava_dir_temp():

    DIR_TEMP = os.path.join(os.getcwd(), 'temp')
    if not os.path.isdir(DIR_TEMP):
        os.mkdir(DIR_TEMP)
    return DIR_TEMP


def tava_dir_parsed(temp):

    DIR_PARSED = os.path.join(temp, 'parsed')
    if not os.path.isdir(DIR_PARSED):
        os.mkdir(DIR_PARSED)
    return DIR_PARSED


def new_tava_file(dir_temp, file_path):

    name = os.path.basename(file_path) + '.tava'
    if not os.path.isdir(dir_temp):
        os.mkdir(dir_temp)

    return os.path.join(dir_temp, name)


def tava_split(file_path):
    return os.path.split(file_path)


def tava_base_name(file_path):
    return os.path.basename(file_path)
