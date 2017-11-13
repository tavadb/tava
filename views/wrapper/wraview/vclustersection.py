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
# Creado:  25/10/2016                                        ###
#                                                            ###
# ##############################################################
'''

import sys
from wx import GetTranslation as L
import wx
from wx.lib.agw import aui
from wx.lib.agw.aui.auibook import AuiNotebook
import wx.lib.agw.ultimatelistctrl as ULC
from wx.lib.pubsub import Publisher as pub

from languages import topic as T
from views.wrapper.wraview.cluster.shape import Shape
from views.wrapper.wraview.cluster.tkmeans import Kmeans


class ClusterSeccion(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        self.SetBackgroundColour('#FFFFFF')

        chec_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # ---- componetes de vistas
        self._checked_all = wx.CheckBox(self, -1, L('SELECT_ALL'))
        self._checked_all.Bind(wx.EVT_CHECKBOX, self.on_checked_all)
        chec_sizer.Add(self._checked_all)

        # ---- ver cabeceras
        self._checked_header = wx.CheckBox(self, -1, L('CHECK_HEADER_CLUSTER'))
        self._checked_header.Bind(wx.EVT_CHECKBOX, self.on_checked_header)
        chec_sizer.Add(self._checked_header)

        _agws = aui.AUI_NB_TOP | aui.AUI_NB_TAB_SPLIT | aui.AUI_NB_TAB_MOVE
        _agws = _agws | aui.AUI_NB_SCROLL_BUTTONS | aui.AUI_NB_DRAW_DND_TAB

        self.nb_clus = AuiNotebook(self, agwStyle=_agws)

        self.shape_list = CheckListCtrlCluster(self.nb_clus, 0)
        self.nb_clus.AddPage(self.shape_list, "Shape")

        self.kmeans_list = CheckListCtrlCluster(self.nb_clus, 1)
        self.nb_clus.AddPage(self.kmeans_list, "Kmeans")
        self.nb_clus.EnableTab(1, False)

        self.shape = None
        self.tkmeans = None
        self.shape_row_index = []
        self.kmeans_row_index = []
        self.pages = [True, False]

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(chec_sizer, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.nb_clus, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(sizer)

    def update_page(self, sh, km):
        self.nb_clus.EnableTab(0, enable=sh)
        self.nb_clus.EnableTab(1, enable=km)

        self.pages = [sh, km]

        if sh and km:
            self.shape_list.DeleteAllItems()
            self.kmeans_list.DeleteAllItems()
            self.shape_row_index = []
            self.kmeans_row_index = []
        if km:
            self.nb_clus.SetSelection(1)
        if sh:
            self.nb_clus.SetSelection(0)

    def generate_shapes(self, df_population, clus, is_nor):
        # ---- generar clusters
        self.shape = Shape(df_population, clus=clus, is_nor=is_nor)

    def generate_kmeans(self, df_population, clus, is_nor):
        # ---- generar clusters
        self.tkmeans = Kmeans(df_population, clus=clus, is_nor=is_nor)

    def update_list(self, c_shape, c_kmenas):

        self._checked_all.SetValue(False)

        # ---- Sección Shape

        if c_shape:
            self.shape_row_index = []
            self.populate_list(self.shape_list, self.shape_row_index,
                               self.shape.clusters)

        # ---- Sección Kmeans
        if c_kmenas:
            # ----- limpiar clusters anteriores
            self.kmeans_row_index = []
            self.populate_list(self.kmeans_list, self.kmeans_row_index,
                               self.tkmeans.clusters)

    def populate_list(self, _list_ctrl, _row_index, _clusters):
        # ----- limpiar clusters anteriores
        _list_ctrl.DeleteAllItems()
        # ---- agregar clusters a la vista
        for c in _clusters:
            index = _list_ctrl.InsertStringItem(sys.maxint, c.name, it_kind=1)

            _list_ctrl.SetStringItem(index, 1, str(c.count))
            _list_ctrl.SetStringItem(index, 2, c.g_percent_format_str())
            _list_ctrl.SetStringItem(index, 3, "")
            _list_ctrl.SetStringItem(index, 4, "")

            _list_ctrl.SetItemData(index, index)
            _row_index.append(index)
#         _list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
#         _list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
        fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR

        for i, c in enumerate(_clusters):
            item = _list_ctrl.GetItem(i, 3)
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(wx.NamedColour(c.clus_color[0]))
            _list_ctrl.SetItem(item)

            item = _list_ctrl.GetItem(i, 4)
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(wx.NamedColour(c.resu_color[0]))
            _list_ctrl.SetItem(item)

    def change_color_cluster(self, index, colour):
        if self.nb_clus.GetSelection() == 0:
            c = self.shape.clusters[index]
            c.clus_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]
        if self.nb_clus.GetSelection() == 1:
            c = self.tkmeans.clusters[index]
            c.clus_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]

    def change_color_summary(self, index, colour):
        if self.nb_clus.GetSelection() == 0:
            c = self.shape.clusters[index]
            c.resu_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]
        if self.nb_clus.GetSelection() == 1:
            c = self.tkmeans.clusters[index]
            c.resu_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]

    def unify_color_cluster(self, colour):
        _colour = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]

        if self.nb_clus.GetSelection() == 0:
            for c in self.shape.clusters:
                c.clus_color = _colour

        if self.nb_clus.GetSelection() == 1:
            for c in self.tkmeans.clusters:
                c.clus_color = _colour

    def unify_color_summary(self, colour):
        _colour = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]

        if self.nb_clus.GetSelection() == 0:
            for c in self.shape.clusters:
                c.resu_color = _colour

        if self.nb_clus.GetSelection() == 1:
            for c in self.tkmeans.clusters:
                c.resu_color = _colour

    def change_group_name(self, index, name):
        if self.nb_clus.GetSelection() == 0:
            c = self.shape.clusters[index]
            c.name = name
        if self.nb_clus.GetSelection() == 1:
            c = self.tkmeans.clusters[index]
            c.name = name
            
    def select_all(self):

        if self.pages[0]:
            for index in self.shape_row_index:
                self.check_item(self.shape_list, index, True)

        if self.pages[1]:
            for index in self.kmeans_row_index:
                self.check_item(self.kmeans_list, index, True)

    def un_select_all(self):
        if self.pages[0]:
            for index in self.shape_row_index:
                self.check_item(self.shape_list, index, False)

        if self.pages[1]:
            for index in self.kmeans_row_index:
                self.check_item(self.kmeans_list, index, False)

    def on_checked_all(self, event):
        if event.IsChecked():
            self.select_all()
        else:
            self.un_select_all()

    def on_checked_header(self, event):
        self.shape_list.on_chech_header(event.IsChecked())
        self.kmeans_list.on_chech_header(event.IsChecked())

    def pre_view(self):

        if self.pages[0]:
            position_checked = []
            position_unchecked = []
            for i, r_i in enumerate(self.shape_row_index):
                if self.shape_list.IsItemChecked(r_i):
                    position_checked.append(i)
                else:
                    position_unchecked.append(i)
            self.shape.cluster_checkeds = position_checked
            self.shape.cluster_uncheckeds = position_unchecked

        if self.pages[1]:
            position_checked = []
            position_unchecked = []

            for i, r_i in enumerate(self.kmeans_row_index):
                if self.kmeans_list.IsItemChecked(r_i):
                    position_checked.append(i)
                else:
                    position_unchecked.append(i)
            self.tkmeans.cluster_checkeds = position_checked
            self.tkmeans.cluster_uncheckeds = position_unchecked

    def contain_elemens(self):

        if self.pages[0]:
            return self.shape_list.GetItemCount()

        if self.pages[1]:
            return self.kmeans_list.GetItemCount()

    def checked_elements(self):

        if self.pages[0]:
            for index in self.shape_row_index:
                if self.shape_list.IsItemChecked(index):
                    return True
            return False

        if self.pages[1]:
            for index in self.kmeans_row_index:
                if self.kmeans_list.IsItemChecked(index):
                    return True
            return False

    def checked_elements_one(self):

        if self.pages[0]:
            for index in self.shape_row_index:
                if self.shape_list.IsItemChecked(index):
                    return True

        if self.pages[1]:
            for index in self.kmeans_row_index:
                if self.kmeans_list.IsItemChecked(index):
                    return True

        return False

    def g_elements(self):
        if self.pages[0]:
            return self.shape.clusters_count

        if self.pages[1]:
            return self.tkmeans.clusters_count

    # ---- funciones para análisis

    def more_representative(self, repre, less_rep):

        self.un_select_all()

        if self.pages[0]:
            # ---- más representativos
            for index in self.shape_row_index[:repre]:
                self.check_item(self.shape_list, index, True)

            # ---- menos representativos
            for index in self.shape_row_index[less_rep:]:
                self.check_item(self.shape_list, index, True)

        if self.pages[1]:
            # ---- más representativos
            for index in self.kmeans_row_index[:repre]:
                self.check_item(self.kmeans_list, index, True)

            # ---- menos representativos
            for index in self.kmeans_row_index[less_rep:]:
                self.check_item(self.kmeans_list, index, True)

    def max_min_objective(self, v_max, v_min):
        self.un_select_all()

        if self.pages[0]:
            for index in self.shape.g_clusters_max_min_in_var(v_max, v_min):
                self.check_item(self.shape_list, index, True)

        if self.pages[1]:
            for index in self.tkmeans.g_clusters_max_min_in_var(v_max, v_min):
                self.check_item(self.kmeans_list, index, True)

    def check_item(self, _list, index, value):
        item = _list.GetItem(index, 0)
        item.Check(value)
        _list.SetItem(item)

    def update_language(self, msg):
        self._checked_all.SetLabel(L('SELECT_ALL'))
        self._checked_header.SetLabel(L('CHECK_HEADER_CLUSTER'))
        self.Layout()

    def s_enable(self, value):
        self._checked_all.Enable(value)
        self._checked_header.Enable(value)

    def selected_by_children(self, page):
        self.nb_clus.SetSelection(page)


class CheckListCtrlCluster(ULC.UltimateListCtrl):

    def __init__(self, parent, page):

        _style = wx.LC_REPORT | wx.LC_SINGLE_SEL | ULC.ULC_BORDER_SELECT
        _style = _style | ULC.ULC_NO_HEADER
        ULC.UltimateListCtrl.__init__(self, parent, wx.ID_ANY, agwStyle=_style)

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        self.currentItem = 0
        self.page = page

        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

        self.InsertColumn(0, L('NAME'), width=78, format=ULC.ULC_FORMAT_CENTER)
        self.InsertColumn(1, 'nro.', width=42, format=ULC.ULC_FORMAT_CENTER)
        self.InsertColumn(2, '%', width=42, format=ULC.ULC_FORMAT_CENTER)
        self.InsertColumn(3, 'c', width=15, format=ULC.ULC_FORMAT_LEFT)
        self.InsertColumn(4, 'r', width=15, format=ULC.ULC_FORMAT_LEFT)

        self.SetColumnToolTip(0, L('NAME_TOLL_TIP'))
        self.SetColumnToolTip(1, L('INDI_BY_CLUSTER'))
        self.SetColumnToolTip(2, L('PORCEN_BY_CLUSTER'))
        self.SetColumnToolTip(3, L('COLOR_CLUSTER'))
        self.SetColumnToolTip(4, L('COLOR_SUMMARY'))

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        self.GetGrandParent().selected_by_children(self.page)

    def OnRightClick(self, event):

        if self.GetItemCount() == 0:
            return

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.on_change_color_clus, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.on_change_color_summ, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.on_unify_color_clus, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.on_unify_color_summ, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.on_change_group_name, id=self.popupID5)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, L('CHANGE_COLOR_CLUSTER'))
        menu.Append(self.popupID2, L('CHANGE_COLOR_SUMMARY'))
        menu.Append(self.popupID3, L('UNIFY_COLOR_CLUSTER'))
        menu.Append(self.popupID4, L('UNIFY_COLOR_SUMMARY'))
        menu.Append(self.popupID5, L('CHANGE_GROUP_NAME'))

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def on_change_color_clus(self, evt):
        item = self.GetItem(self.currentItem, 3)
        colour = item.GetBackgroundColour()
        c = wx.ColourData()
        c.SetColour(colour)
        dlg = wx.ColourDialog(self, c)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR
            data = dlg.GetColourData()
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(data.GetColour())
            self.SetItem(item)
            self.GetParent().GetParent().change_color_cluster(self.currentItem,
                                                              data.GetColour())

        dlg.Destroy()

    def on_unify_color_clus(self, evt):

        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            c_colour = dlg.GetColourData().GetColour()

            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)

            for i in range(self.GetItemCount()):
                item = self.GetItem(i, 3)
                item.SetMask(fullMask)
                item.SetFont(font)
                item.SetBackgroundColour(c_colour)
                self.SetItem(item)

            self.GetParent().GetParent().unify_color_cluster(c_colour)

        dlg.Destroy()

    def on_change_color_summ(self, evt):
        item = self.GetItem(self.currentItem, 4)
        colour = item.GetBackgroundColour()
        c = wx.ColourData()
        c.SetColour(colour)
        dlg = wx.ColourDialog(self, c)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR
            data = dlg.GetColourData()
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(data.GetColour())
            self.SetItem(item)
            self.GetParent().GetParent().change_color_summary(self.currentItem,
                                                              data.GetColour())

        dlg.Destroy()

    def on_unify_color_summ(self, evt):

        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            c_colour = dlg.GetColourData().GetColour()

            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)

            for i in range(self.GetItemCount()):
                item = self.GetItem(i, 4)
                item.SetMask(fullMask)
                item.SetFont(font)
                item.SetBackgroundColour(c_colour)
                self.SetItem(item)

            self.GetParent().GetParent().unify_color_summary(c_colour)

        dlg.Destroy()
        
    def on_change_group_name(self, evt):

        item = self.GetItem(self.currentItem, 0)
        g_label = item.GetText();
        dlg = wx.TextEntryDialog(
                self, L('CHANGE_GROUP_NAME_D'),
                L('CHANGE_GROUP_NAME_T'), 'Python')
        dlg.SetValue(g_label)
 
        if dlg.ShowModal() == wx.ID_OK:
            if len(dlg.GetValue().strip()) != 0:
                item.SetText(dlg.GetValue())
                self.SetItem(item)
                self.GetParent().GetParent().change_group_name(self.currentItem,
                                                               dlg.GetValue())
        dlg.Destroy()

    def on_chech_header(self, see):
        _style = wx.LC_REPORT | wx.LC_SINGLE_SEL | ULC.ULC_BORDER_SELECT
        if see:
            self.SetAGWWindowStyleFlag(_style)
        else:
            _style = _style | ULC.ULC_NO_HEADER
            self.SetAGWWindowStyleFlag(_style)

    def update_language(self, msg):

        self.SetColumnToolTip(0, L('NAME_TOLL_TIP'))
        self.SetColumnToolTip(1, L('INDI_BY_CLUSTER'))
        self.SetColumnToolTip(2, L('PORCEN_BY_CLUSTER'))
        self.SetColumnToolTip(3, L('COLOR_CLUSTER'))
        self.SetColumnToolTip(4, L('COLOR_SUMMARY'))
