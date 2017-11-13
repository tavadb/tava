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
# Creado:  18/9/2015                                         ###
#                                                            ###
# ##############################################################
'''


class TavaException(Exception):
    """Clase base para excepciones en Tava."""
    pass


class TavaError(TavaException):

    """Clase base para excepciones en TAVA."""
    def __init__(self, filename, message, errorline):
        self.filename = filename
        self.message = message
        self.errorline = errorline

    def __repr__(self):
        return "<TavaError(filename='%s', message='%s',\
        error line='%s')>" % (self.filename, self.message, self.errorline)


class ParserError(TavaError):

    """Clase base para manejo de excepciones de parseo"""

    def __init__(self, filename, message, errorline):
        TavaError.__init__(self, filename, message, errorline)

    def __repr__(self):
        return "<ParserError(filename='%s', message='%s',\
        error line='%s')>" % (self.filename, self.message, self.errorline)


class PreParserError(TavaError):

    '''
    Excepción lanzada por errores en el preparseo.

    :param filename: path absoluto con nombre del archivo
    :type str:
    :param mensaje: mensaje de error
    :type str:
    '''

    def __init__(self, filename, message, errorline):
        TavaError.__init__(self, filename, message, errorline)

    def __repr__(self):
        return "<PreParserError(filename='%s', message='%s',\
        error line='%s')>" % (self.filename, self.message, self.errorline)
