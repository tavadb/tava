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
from wx.lib.itemspicker import ItemsPicker, EVT_IP_SELECTION_CHANGED


K_MENU_ITEM_DATA_BLOCK = 0
K_MENU_ITEM_DATA_SUBBLOCK = 1


class BlockSorted(wx.Dialog):

    def __init__(self, parent, _names):
        wx.Dialog.__init__(self, parent, size=(400, 300),
                           title='Ordenar Bloques')
        self.parent = parent
        self.names = _names
        self.init_ui()

        # ------ Definiciones iniciales -----

        self.Centre(wx.BOTH)
        self.CenterOnScreen()
        self.ShowModal()

    def init_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        # titulo
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label='Ordenando Bloques')
        title_line = wx.StaticLine(self)
        title_sizer.Add(title, 0, wx.CENTER | wx.TOP, 10)
        title_sizer.Add(title_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        self.i_picker = ItemsPicker(self, -1, self.names, 'Orden actual',
                                    'Nuevo Orden')

        # buttons confirmar, cancelar
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cancel = wx.BoxSizer()
        self.cancel = wx.Button(self, -1, 'Cancelar')
        self.cancel.SetDefault()
        sizer_cancel.Add(self.cancel)
        sizer_apply = wx.BoxSizer()
        self.apply = wx.Button(self, -1, 'Aplicar')
        sizer_apply.Add(self.apply, 0, wx.ALIGN_RIGHT)
        self.apply.Disable()

        sizer_button.Add(sizer_cancel, 0, wx.ALL, 5)
        sizer_button.Add(sizer_apply, 0, wx.ALL, 5)

        sizer.Add(title_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        sizer.Add(self.i_picker, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_button, 0, wx.EXPAND | wx.LEFT, 100)

        self.i_picker.Bind(EVT_IP_SELECTION_CHANGED, self.check_up)
        self.Bind(wx.EVT_BUTTON, self.on_button_apply, self.apply)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, self.cancel)
        self.Bind(wx.EVT_CHAR, self.on_key_escape)

        self.SetSizer(sizer)

    def check_up(self, event):

        if len(self.names) != len(self.i_picker.GetSelections()):
            self.apply.Disable()
            self.cancel.SetDefault()
            return None

        _names = [str(i) for i in self.i_picker.GetSelections()]
        if self.names == _names:
            self.apply.Disable()
            self.cancel.SetDefault()
            return None

        self.apply.Enable()
        self.apply.SetDefault()

    def on_button_cancel(self, event):
        self.Close()

    def on_button_apply(self, event):
        order = [str(i) for i in self.i_picker.GetSelections()]
        new_order = []
        for name in self.names:
            new_order.append(order.index(name))
        self.parent.sort_blocks(new_order)
        self.Close()

    def on_key_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()


class KMenuBlocks(wx.Menu):
    '''
    '''
    def __init__(self, parent):

        wx.Menu.__init__(self)
        self.parent = parent

        self.init_ui()

    def init_ui(self):

        _order_block = wx.MenuItem(self, wx.ID_ANY, "Ordenar Bloques")
        self.AppendItem(_order_block)
        self.Bind(wx.EVT_MENU, self.on_order_block, _order_block)

        _order_subblock = wx.MenuItem(self, wx.ID_ANY, "Ordenar SubBloques")
        self.AppendItem(_order_subblock)
        self.Bind(wx.EVT_MENU, self.on_order_subblock, _order_subblock)

    def on_order_block(self, event):
        self.parent.menu_block = K_MENU_ITEM_DATA_BLOCK

    def on_order_subblock(self, event):
        self.parent.menu_block = K_MENU_ITEM_DATA_SUBBLOCK


class SubBlockSorted(wx.Dialog):

    def __init__(self, parent, _names, item):
        wx.Dialog.__init__(self, parent, size=(400, 300),
                           title='Ordenar Sub Bloques')
        self.parent = parent
        self.names = _names
        self.item = item
        self.init_ui()

        # ------ Definiciones iniciales -----

        self.Centre(wx.BOTH)
        self.CenterOnScreen()
        self.ShowModal()

    def init_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        # titulo
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label='Ordenando SubBloques')
        title_line = wx.StaticLine(self)
        title_sizer.Add(title, 0, wx.CENTER | wx.TOP, 10)
        title_sizer.Add(title_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        self.i_picker = ItemsPicker(self, -1, self.names, 'Orden actual',
                                    'Nuevo Orden')

        # buttons confirmar, cancelar
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cancel = wx.BoxSizer()
        self.cancel = wx.Button(self, -1, 'Cancelar')
        self.cancel.SetDefault()
        sizer_cancel.Add(self.cancel)
        sizer_apply = wx.BoxSizer()
        self.apply = wx.Button(self, -1, 'Aplicar')
        sizer_apply.Add(self.apply, 0, wx.ALIGN_RIGHT)
        self.apply.Disable()

        sizer_button.Add(sizer_cancel, 0, wx.ALL, 5)
        sizer_button.Add(sizer_apply, 0, wx.ALL, 5)

        sizer.Add(title_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        sizer.Add(self.i_picker, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_button, 0, wx.EXPAND | wx.LEFT, 100)

        self.i_picker.Bind(EVT_IP_SELECTION_CHANGED, self.check_up)
        self.Bind(wx.EVT_BUTTON, self.on_button_apply, self.apply)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, self.cancel)
        self.Bind(wx.EVT_CHAR, self.on_key_escape)

        self.SetSizer(sizer)

    def check_up(self, event):

        if len(self.names) != len(self.i_picker.GetSelections()):
            self.apply.Disable()
            self.cancel.SetDefault()
            return None

        _names = [str(i) for i in self.i_picker.GetSelections()]
        if self.names == _names:
            self.apply.Disable()
            self.cancel.SetDefault()
            return None

        self.apply.Enable()
        self.apply.SetDefault()

    def on_button_cancel(self, event):
        self.Close()

    def on_button_apply(self, event):
        order = [str(i) for i in self.i_picker.GetSelections()]
        new_order = []
        for name in self.names:
            new_order.append(order.index(name))
        self.parent.sort_subblocks(new_order, self.item)
        self.Close()

    def on_key_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
