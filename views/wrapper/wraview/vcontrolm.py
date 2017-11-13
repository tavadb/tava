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

import wx
from wx.lib.agw.genericmessagedialog import GenericMessageDialog
from wx.lib.agw.genericmessagedialog import GMD_USE_GRADIENTBUTTONS
from wx import GetTranslation as L


KMSG_EMPTY_DATA_SELECTED = 0
KMSG_EMPTY_CLUSTER_DATA = 3
KMSG_EMPTY_CLUSTER_SELECTED = 4
KMSG_EMPTY_DATA_GENERATE_CLUSTER = 5
KMSG_GENERATE_CLUSTER = 6
KMSG_EMPTY_NUMBER_KMEANS = 7
KMSG_INVALID_NUM_CLUSTERS = 8


K_ICON_INFORMATION = wx.ICON_INFORMATION
K_ICON_QUESTION = wx.ICON_QUESTION
K_ICON_ERROR = wx.ICON_ERROR
K_ICON_HAND = wx.ICON_HAND
K_ICON_EXCLAMATION = wx.ICON_EXCLAMATION

K_OK = wx.OK
K_CANCEL = wx.CANCEL
K_YES_NO = wx.YES_NO
K_YES_DEFAULT = wx.YES_DEFAULT
K_NO_DEFAULT = wx.NO_DEFAULT


class KMessage():

    def __init__(self, parent, key_message, key_ico=K_ICON_INFORMATION,
                 key_button=K_OK):

        self.parent = parent

        if key_message == KMSG_EMPTY_DATA_SELECTED:
            self.h_msg = L('H_EMPTY_DATA_SELECTED')
            self.m_msg = L('EMPTY_DATA_SELECTED')
            self.k_ico = key_ico
            self.k_but = key_button
        elif key_message == KMSG_EMPTY_CLUSTER_DATA:
            self.h_msg = L('H_EMPTY_CLUSTER_DATA')
            self.m_msg = L('EMPTY_CLUSTER_DATA')
            self.k_ico = key_ico
            self.k_but = key_button
        elif key_message == KMSG_EMPTY_CLUSTER_SELECTED:
            self.h_msg = L('H_EMPTY_CLUSTER_SELECTED')
            self.m_msg = L('EMPTY_CLUSTER_SELECTED')
            self.k_ico = key_ico
            self.k_but = key_button
        elif key_message == KMSG_EMPTY_DATA_GENERATE_CLUSTER:
            self.h_msg = L('H_EMPTY_DATA_GENERATE_CLUSTER')
            self.m_msg = L('EMPTY_EMPTY_DATA_GENERATE_CLUSTER')
            self.k_ico = key_ico
            self.k_but = key_button
        elif key_message == KMSG_GENERATE_CLUSTER:
            self.h_msg = L('H_GENERATE_CLUSTER')
            self.m_msg = L('EMPTY_GENERATE_CLUSTER')
            self.k_ico = key_ico
            self.k_but = key_button

        elif key_message == KMSG_EMPTY_NUMBER_KMEANS:
            self.h_msg = L('H_EMPTY_NUMBER_KMEANS')
            self.m_msg = L('EMPTY_NUMBER_KMEANS')
            self.k_ico = key_ico
            self.k_but = key_button

        elif key_message == KMSG_INVALID_NUM_CLUSTERS:
            self.h_msg = L('H_INVALID_NUM_CLUSTERS')
            self.m_msg = L('INVALID_NUM_CLUSTERS')
            self.k_ico = key_ico
            self.k_but = key_button

        else:
            self.h_msg = 'Defaul'
            self.m_msg = 'Defaul'
            self.k_ico = key_ico
            self.k_but = key_button

    def kshow(self):
        dlg = GenericMessageDialog(self.parent, self.m_msg,
                                   self.h_msg,
                                   self.k_ico | self.k_but |
                                   GMD_USE_GRADIENTBUTTONS)
        dlg.ShowModal()
        dlg.Destroy()
