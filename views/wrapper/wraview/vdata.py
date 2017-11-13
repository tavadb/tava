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


import sys
import wx

import wx.lib.agw.aui as aui
import wx.lib.mixins.listctrl as listmix
from imgs.iview import smiles, small_up_arrow, small_dn_arrow


KURI_AUI_NB_STYLE_DATA = aui.AUI_NB_BOTTOM | aui.AUI_NB_TAB_SPLIT | \
    aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS |\
    aui.AUI_NB_MIDDLE_CLICK_CLOSE | aui.AUI_NB_DRAW_DND_TAB

K_INDEX_PAGE_DATA = 0
K_INDEX_PAGE_INFO = 1


class DataPanel(aui.AuiNotebook):
    def __init__(self, parent):
        aui.AuiNotebook.__init__(self, parent, agwStyle=KURI_AUI_NB_STYLE_DATA)
        self.SetBackgroundColour('#AAA666')
        self.SetArtProvider(aui.VC71TabArt())

        self.count_datas = 0
        self.count_selected_datas = 0

        self.data_seccion, self.count_datas = self.g_data_list()
        self.InsertPage(K_INDEX_PAGE_DATA, self.data_seccion,
                        "Datos Visualizados", select=True)

        self.InsertPage(K_INDEX_PAGE_INFO, wx.StaticText(self),
                        self.g_selected_mss())
        self.EnableTab(K_INDEX_PAGE_INFO, False)

        self.Fit()

    def kadd(self, df):

        if self.GetPageCount():
            self.DeletePage(K_INDEX_PAGE_INFO)
            self.DeletePage(K_INDEX_PAGE_DATA)

        data_seccion, self.count_datas = self.g_data_list(df)
        self.InsertPage(K_INDEX_PAGE_DATA, data_seccion,
                        "Datos Visualizados", select=True)

        self.InsertPage(K_INDEX_PAGE_INFO, wx.StaticText(self),
                        self.g_selected_mss())
        self.EnableTab(K_INDEX_PAGE_INFO, False)

        self.data_seccion = data_seccion

    def g_data_list(self, df=None):
        _data = TestListCtrlPanel(self, df)
        df = [] if df is None else df
        return _data, len(df)

    def update_mss_count_selected(self, csd):
        self.count_selected_datas = csd
        self.SetPageText(K_INDEX_PAGE_INFO, self.g_selected_mss())

    def g_selected_mss(self):
        csd = self.count_selected_datas
        return "Count:" + str(self.count_datas) + " / selected:" + str(csd)


class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, df=None):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        if df is not None:
            return self.populate(df)

        self.len_columns = 0
        self.df_dict = {}

    def populate(self, df):
        df['id'] = range(len(df.index))

        # add columns
        _cols = list(df.columns.values)
        _cols = _cols[0:len(_cols)-1]
        for ic in range(len(_cols)):
            self.InsertColumn(ic, _cols[ic], wx.LIST_FORMAT_CENTER)

        # add dates
        for v in df.values.tolist():
            vv = [str(_v) for _v in v]
            pos = 0
            index = 0
            _key = 0
            for vvv in vv[0:len(vv)-1]:
                if pos == 0:
                    index = self.InsertStringItem(sys.maxint, vvv)
                else:
                    self.SetStringItem(index, pos, vvv)
                pos += 1
                _key = vv[pos]
            self.SetItemData(index, int(_key))

        # formate columns
        for ic in range(len(_cols)):
            self.SetColumnWidth(ic, wx.LIST_AUTOSIZE)

        self.len_columns = len(df.columns)
        self.df_dict = df.set_index('id').T.to_dict('list')


class TestListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, df=None):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.parent = parent

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.il = wx.ImageList(16, 16)

        self.idx1 = self.il.Add(smiles.GetBitmap())
        self.sm_up = self.il.Add(small_up_arrow.GetBitmap())
        self.sm_dn = self.il.Add(small_dn_arrow.GetBitmap())

        self.d_list = TestListCtrl(self, wx.NewId(), style=wx.LC_REPORT |
                                   wx.BORDER_NONE | wx.LC_SORT_ASCENDING,
                                   df=df)

        self.d_list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.itemDataMap = self.d_list.df_dict
        listmix.ColumnSorterMixin.__init__(self, self.d_list.len_columns)

        sizer.Add(self.d_list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.d_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.d_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)

    def GetListCtrl(self):
        return self.d_list

    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

    def OnItemSelected(self, event):
        item = self.d_list.GetFirstSelected()
        if -1 == item:
            self.parent.update_mss_count_selected(0)
        else:
            rows_selected = 0
            while item != -1:
                rows_selected += 1
                item = self.d_list.GetNextSelected(item)
            self.parent.update_mss_count_selected(rows_selected)

    def OnItemDeselected(self, event):
        print 'Item deseleccionados'
