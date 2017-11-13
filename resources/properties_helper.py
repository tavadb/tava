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
# Creado:  30/8/2016                                         ###
#                                                            ###
# ##############################################################
'''

import os


class PropertiesHelper():

    def __init__(self):

        _path = os.path.join(os.getcwd(), 'properties')
        self.path_propertie = os.path.join(_path, 'tava.conf')

    def read_values(self):
        f = open(self.path_propertie, 'r')
        values = {}
        for _line in f.readlines():
            _key, _value = _line.strip().split('=')
            values[_key] = _value
        f.close()

        return values

    def write_values(self, values):
        f = open(self.path_propertie, 'w')
        for _key in values.keys():
            _line = '='.join([_key, values[_key]]) + '\n'
            f.write(_line)
        f.close()

    def get_by_key(self, key_value):
        values = self.read_values()
        return values[key_value]

    def set_by_key(self, key_value, new_value):
        values = self.read_values()
        values[key_value] = new_value
        self.write_values(values)

    def get_search_result(self):
        _path = self.get_by_key('SEARCH_RESULT')
        if os.path.exists(_path):
            return _path
        return os.path.expanduser("~")

    def set_search_result(self, new_value):
        self.set_by_key('SEARCH_RESULT', new_value)

    def get_file_format(self):
        return int(self.get_by_key('FILE_FORMAT'))

    def set_file_format(self, new_value):
        self.set_by_key('FILE_FORMAT', str(new_value))

    def get_file_format_sep(self):
        return int(self.get_by_key('FILE_FORMAT_SEP'))

    def set_file_format_sep(self, new_value):
        self.set_by_key('FILE_FORMAT_SEP', str(new_value))

    def get_language(self):
        return str(self.get_by_key('LANGUAGE'))

    def set_language(self, new_value):
        self.set_by_key('LANGUAGE', str(new_value))
