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
# Creado:  1/9/2016                                          ###
#                                                            ###
# ##############################################################
'''

from pandas.core.frame import DataFrame
import wx

from views.wrapper.wraview.vcontrol import ControlPanel, KBlock
from views.wrapper.wraview.vfigure import FigurePanel


K_COLUMN_NAMES = 'K_COLUMN_NAMES'
K_BLOCK_DATAS = 'K_BLOCK_DATAS'
K_BLOCK_NAMES = 'K_BLOCK_NAMES'
K_SUB_BLOCK_NAMES = 'K_SUB_BLOCK_NAMES'


class ViewMainPanel(wx.Panel):

    def __init__(self, parent, view):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.view = view

        self._init()

        sizer = wx.BoxSizer()
        sizer.Add(self.splitter, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def _init(self):

        ksub_blocks = self.transform_data()

        self.splitter = wx.SplitterWindow(self, style=wx.SP_3D)

        # -------------- GRAFICOS IZQUIERDO - LEFT GRAFICOS----------
        # -------     gŕaficos estableccidos para aplicación   -----
        # ----------------------------------------------------------
        self.kfigure = FigurePanel(self.splitter)

#         self.split1 = wx.SplitterWindow(self.splitter, style=wx.SP_3D)
#         self.kfigure = FigurePanel(self.split1)
#         self.kdata = DataPanel(self.split1)
#
#         self.split1.SplitHorizontally(self.kfigure, self.kdata, 700)
#         self.split1.SetMinimumPaneSize(110)
#         self.split1.SetSashGravity(0.7)

        # -------------- MENU DERECHO - RIGHT MENU   --------------
        # -------     opciones de gŕaficos definidos aqui    -------
        # ----------------------------------------------------------
        self.control = ControlPanel(self.splitter, self.kfigure,
                                    ksub_blocks, self)
        self.kfigure.control_panel = self.control

        self.splitter.SplitVertically(self.kfigure, self.control, 630)
#         self.splitter.SetMinimumPaneSize(10)
        self.splitter.SetSashGravity(0.9)

    def transform_data(self):
        kblocks = {}
        ri_key = 0

        #  obtener arcivos de la vista
        for ir, vres in enumerate(self.view.results):
            res = vres.result

            for vite in vres.iterations:
                ite = vite.iteration
                _block = []
                for indi in ite.individuals:
                    objective = [float(i) for i in indi.objectives.split(',')]
                    objective.append(str(ite.number))
                    _block.append(objective)
                column_level = [nm for nm in res.name_objectives.split(',')]
                column_level.append('Name')
                df = DataFrame(_block, columns=column_level)
                # sub_blocks.append(KBlock(str(ite.number), df))
                kname = 'r' + str(ir + 1) + ' - b' + str(ite.number)
                kblocks[ri_key] = (kname, KBlock(str(ite.number), df))
                ri_key += 1

        return kblocks
