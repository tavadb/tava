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
# Creado:  1/9/2016                                        ###
#                                                            ###
# ##############################################################
'''

from pandas.tools.plotting import _get_standard_colors


def square_plot(plots, cc=True):
    s_col = 1
    s_row = 1
    while (s_col*s_row) < plots:
        if cc:
            s_col += 1
            cc = False
        else:
            s_row += 1
            cc = True
    return s_row, s_col


def g_colors(count, color):
    color_values = _get_standard_colors(count, None, 'random', color)
    return color_values
