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


import wx
from wx.lib.agw import customtreectrl as CT

from views.wrapper.wraview.vfigure import K_PARALLEL_COORDENATE, \
    K_ANDREWS_CURVES, K_RADVIZ, K_RADAR_CHART_CIRCLE, K_RADAR_CHART_POLYGON, \
    K_SCATTER_MATRIX, K_SOM, K_HITMAP


KURI_TR_STYLE2 = CT.TR_HIDE_ROOT | CT.TR_NO_LINES


K_FIGURES_1D = ['Lineas 3D', 'Scatter 3D', 'Barras vertical 3D',
                'Poligono', 'Puntos', 'Lineas', 'Puntos y lineas',
                'Barras vertical', 'Barras horizontal',
                'Histogram vertical', 'Histogram horizontal',
                'Boxplot vertical', 'Boxplot horizontal',
                'Density Estimation', 'Density',
                'Area', 'Stem']


# -------------------                                  ------------------------
class FigureManyD(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent, -1, wx.Point(0, 0),
                                   wx.Size(220, 250))

        self.SetAGWWindowStyleFlag(KURI_TR_STYLE2)
        self.root = self.AddRoot('ROOT-FIGURES')
        self.init_ui()

    def init_ui(self):

        r_item = self.AppendItem(self.root, 'Coodenadas Paralelas', ct_type=2)
        self.SetItemPyData(r_item, K_PARALLEL_COORDENATE)
        r_item.Check()
        r_item = self.AppendItem(self.root, 'Andrews Curves', ct_type=2)
        self.SetItemPyData(r_item, K_ANDREWS_CURVES)

        r_item = self.AppendItem(self.root, 'Radviz', ct_type=2)
        self.SetItemPyData(r_item, K_RADVIZ)
        r_item = self.AppendItem(self.root, 'Radar Chart Circle', ct_type=2)
        self.SetItemPyData(r_item, K_RADAR_CHART_CIRCLE)
        r_item = self.AppendItem(self.root, 'Radar Chart Polygon', ct_type=2)
        self.SetItemPyData(r_item, K_RADAR_CHART_POLYGON)

        self.AppendSeparator(self.root)

        r_item = self.AppendItem(self.root, 'Scatter Matrix', ct_type=2)
        self.SetItemPyData(r_item, K_SCATTER_MATRIX)
        r_item = self.AppendItem(self.root, 'SOM', ct_type=2)
        self.SetItemPyData(r_item, K_SOM)
        self.EnableItem(r_item, False)
        r_item = self.AppendItem(self.root, 'HITMAP', ct_type=2)
        self.SetItemPyData(r_item, K_HITMAP)
        self.EnableItem(r_item, False)

        self.ExpandAllChildren(self.root)

    def g_key_figure(self):

        for fig in self.root.GetChildren():
            if fig.IsChecked():
                return fig.GetData()
        return 0


# -------------------                                  ------------------------
class Figure1D(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent, -1, wx.Point(0, 0),
                                   wx.Size(220, 250))

        self.SetAGWWindowStyleFlag(KURI_TR_STYLE2)
        self.root = self.AddRoot('ROOT_FIGURES_1D')
        self.init_ui()

    def init_ui(self):

        r_item = self.AppendItem(self.root, 'Lineas 3D', ct_type=2)
        self.SetItemPyData(r_item, K_PARALLEL_COORDENATE)
        r_item.Check()
        r_item = self.AppendItem(self.root, 'Scatter 3D', ct_type=2)
        self.SetItemPyData(r_item, K_ANDREWS_CURVES)

        r_item = self.AppendItem(self.root, 'Barras vertical 3D', ct_type=2)
        self.SetItemPyData(r_item, K_RADVIZ)
        r_item = self.AppendItem(self.root, 'Poligono', ct_type=2)
        self.SetItemPyData(r_item, K_RADAR_CHART_CIRCLE)

        self.AppendSeparator(self.root)

        r_item = self.AppendItem(self.root, 'Puntos', ct_type=2)
        self.SetItemPyData(r_item, K_RADAR_CHART_POLYGON)
        r_item = self.AppendItem(self.root, 'Lineas', ct_type=2)
        self.SetItemPyData(r_item, K_SCATTER_MATRIX)
        r_item = self.AppendItem(self.root, 'Puntos y lineas', ct_type=2)
        self.SetItemPyData(r_item, K_SOM)
        self.EnableItem(r_item, False)
        r_item = self.AppendItem(self.root, 'Barras vertical', ct_type=2)
        self.SetItemPyData(r_item, K_HITMAP)
        self.EnableItem(r_item, False)

        self.ExpandAllChildren(self.root)

    def g_key_figure(self):

        for fig in self.root.GetChildren():
            if fig.IsChecked():
                return fig.GetData()
        return 0


class FigureD(wx.CheckListBox):
    def __init__(self, parent, K_FIGURES_1D):
        wx.CheckListBox.__init__(self, parent, -1, choices=K_FIGURES_1D)
