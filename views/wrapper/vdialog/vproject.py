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
import sys
from wx import GetTranslation as L
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from wx.lib.pubsub import Publisher as pub

from imgs.iproject import execute_bit, help32x32_bit, error_bit
from languages import topic as T
from models.mproject import ProjectM
import wx.dataview as dv


class NewProject(wx.Dialog):
    def __init__(self, parent, properties, add_result=False):
        wx.Dialog.__init__(self, parent, size=(700, 630))

        self.error_name = True
        self.add_result = add_result
        self.parent = parent

        self.properties = properties

        self.wildcard = L('FILES_RESULTS') + " |*"

        self.FILES_FORMATS = [' Von Tava', L('SEPARATOR') + ':']

        self.SEPARATOR_FILE = [', ' + L('COMMA'), '; ' + L('SEMICOLON'), '  '
                               + L('BLANK_SPACE'), '- ' + L('HYPHEN'), '_ ' +
                               L('UNDERSCORE')]
        self.SEPARATOR_FILE_VALUE = [',', ';', ' ', '-', '_']

        self.existing_names = []
        self.hidden_names = []
        self.path_files = []
        self.InitUI()
        self.create.Disable()
        if add_result:
            self.add_only_results()
        self.Centre()
        self.ShowModal()

    def InitUI(self):

        # ------ variables principales --------------------------------------
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(8, 5)

        # ------ Titulo de Proyecto Tava ------------------------------------
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(14)
        title1 = wx.StaticText(panel, label=L('NEW_PROJECT_TITLE'))
        title1.SetFont(font_title)

        exec_bmp = wx.StaticBitmap(panel)

        sizer.Add(title1, pos=(0, 0), flag=wx.LEFT | wx.TOP |
                  wx.ALIGN_LEFT, border=10)
        sizer.Add(exec_bmp, pos=(0, 4), flag=wx.ALIGN_CENTER)

        # ------ Texto Descriptivo que cambia --------------------------------
        des_box = wx.BoxSizer(wx.HORIZONTAL)

        font_description = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_description.SetPointSize(9)
        self.alert_text = wx.StaticText(panel)
        self.alert_text.SetFont(font_description)
        self.alert_text.SetLabel(L('NEW_PROJECT_ENTER_NAME'))

        self.alert_bmp = wx.StaticBitmap(panel)
        self.alert_bmp.SetBitmap(execute_bit.GetBitmap())

        des_box.Add(self.alert_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        des_box.Add(self.alert_text, flag=wx.ALIGN_LEFT)

        sizer.Add(des_box, pos=(1, 0), span=(1, 3), flag=wx.LEFT, border=10)

        # ------ linea estática horizontal -----------------------------------
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 5), flag=wx.EXPAND |
                  wx.ALIGN_TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # ------ Texto para nombre de proyecto ------------------------------
        label = wx.StaticText(panel, label=L('NEW_PROJECT_NAME'))

        sizer.Add(label, pos=(3, 0), flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        self.name = wx.TextCtrl(panel)
        self.name.SetBackgroundColour((255, 255, 255))
        self.name.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.name.SetFocus()

        sizer.Add(self.name, pos=(3, 1), span=(1, 4),
                  flag=wx.EXPAND | wx.RIGHT, border=10)

        # ------ Agregacion de archivo  (x, y)-------------------------------
        sb = wx.StaticBox(panel, label=L('FILE_STATIC_LABEL'))
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        # boton para busqueda (1)
        browse = wx.Button(panel, -1, L('FILE_BUTTON_BROWSER'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonBrowse, browse)
        boxsizer.Add(browse, flag=wx.ALIGN_LEFT | wx.TOP | wx.BOTTOM, border=5)

        # grilla de archivos (2)
        self.dvlc = dv.DataViewListCtrl(panel, size=(400, 298))
        self.dvlc.AppendTextColumn(L('FILE_LABEL_COL_NAME'), width=250)
        self.dvlc.AppendTextColumn(L('FILE__COL_DIRECTORY'), width=150)
        boxsizer.Add(self.dvlc, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=2)

        # ---- selección de formato

        self.radio_von = wx.RadioButton(panel, -1, self.FILES_FORMATS[0],
                                        style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_von, self.radio_von)
        self.radio_sep = wx.RadioButton(panel, -1, self.FILES_FORMATS[1])
        self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_sep, self.radio_sep)
        p_sep = self.properties.get_file_format_sep()
        self.cb_sep = wx.ComboBox(panel, 500, self.SEPARATOR_FILE[p_sep], (90, 50),
                                  (160, -1), self.SEPARATOR_FILE, wx.CB_DROPDOWN)
        sep_sizer = wx.BoxSizer()
        sep_sizer.Add(self.radio_sep)
        sep_sizer.Add(self.cb_sep)
        self.set_option_radio()

        s_sizer = wx.BoxSizer(wx.HORIZONTAL)
        s_sizer.Add(self.radio_von, 0, wx.EXPAND)
        s_sizer.Add(sep_sizer, 0, wx.EXPAND)
        boxsizer.Add(s_sizer, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM,
                     border=10)

        sizer.Add(boxsizer, pos=(4, 0), span=(1, 5), flag=wx.RIGHT |
                  wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        # ------ Buttons foot -----------------------------------------------
        help_p = wx.BitmapButton(panel, bitmap=help32x32_bit.GetBitmap(),
                                 style=wx.NO_BORDER)
        sizer.Add(help_p, pos=(5, 0), span=(1, 3),
                  flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
        # help_p.Bind(wx.EVT_BUTTON, self.OnHelpP)

        cancel = wx.Button(panel,
                           label=L('NEW_PROJECT_CANCEL'), size=(125, 32))
        sizer.Add(cancel, pos=(5, 3), flag=wx.ALIGN_BOTTOM | wx.RIGHT,
                  border=25)
        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.create = wx.Button(panel, label=L('NEW_PROJECT_OK'),
                                size=(125, 32))
        sizer.Add(self.create, pos=(5, 4), flag=wx.ALIGN_BOTTOM |
                  wx.RIGHT | wx.LEFT, border=10)
        self.create.Bind(wx.EVT_BUTTON, self.on_create)

        # ------ configuraciones Globales -----------------------------------
        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

        panel.Bind(wx.EVT_CHAR, self.on_key_down)

        # self.existing_names = ProjectM().names_not_hidden()
        # self.hidden_names = ProjectM().names_hidden()

    def on_radio_von(self, event):
        self.cb_sep.Disable()

    def on_radio_sep(self, event):
        self.cb_sep.Enable()

    def set_option_radio(self):
        option = self.properties.get_file_format()
        if option == 0:
            self.radio_von.SetValue(True)
            self.cb_sep.Disable()
        elif option == 1:
            self.radio_sep.SetValue(True)
            self.cb_sep.Enable()

    def update_selected_formate(self):
        if self.radio_von.GetValue():
            self.properties.set_file_format(0)
            self.parent.p_formate = 0
        elif self.radio_sep.GetValue():
            self.properties.set_file_format(1)
            i_value = self.SEPARATOR_FILE.index(self.cb_sep.GetValue())
            self.properties.set_file_format_sep(i_value)
            self.parent.p_formate = 1
            self.parent.p_sep = self.SEPARATOR_FILE_VALUE[i_value]

    def add_only_results(self):
        self.alert_text.SetLabel(L('ADD_FILE_RESULT_HEADER'))
        self.name.SetValue(self.parent.p_project.name)
        self.name.Disable()

        self.create.SetLabel(L('ADD_FILE_RESULT'))
        self.create.Enable()
        pass

    def on_cancel(self, event):
        self.parent.p_create = False
        self.Close()

    def on_create(self, event):
        if not self.add_result:
            self.parent.p_name = self.name.GetValue()
            for p in self.path_files:
                _, name = os.path.split(p)
                self.parent.p_path_files.append([p, name])
        else:
            if len(self.path_files) > 0:
                for p in self.path_files:
                    _, name = os.path.split(p)
                    self.parent.p_path_files.append([p, name])
            else:
                self.parent.p_create = False

        self.parent.p_create = True
        self.update_selected_formate()
        self.Close()

    def on_key_down(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.parent.p_create = False
            self.Close()

    def on_key_up(self, event):

        key_code = event.GetKeyCode()

        if key_code == wx.WXK_ESCAPE:
            self.parent.p_create = False
            self.Close()

        elif key_code == wx.WXK_RETURN:
            # verificar si se puede crear
            if not self.error_name:
                self.on_create(None)

        else:
            # verificar caracteres permitidos para nombre

            name = self.name.GetValue()
            self.error_name = False
            self.create.Enable()
            error_message = ''

            if len(name) == 0:
                self.alert_text.SetLabel(L('NEW_PROJECT_ENTER_NAME'))
                self.alert_bmp.SetBitmap(execute_bit.GetBitmap())
                self.name.SetBackgroundColour('#FFFFFF')
                self.error_name = True
                self.create.Disable()
                return None

            if len(name.strip(' ')) == 0:
                self.alert_text.SetLabel(L('NEW_PRO_BLANK_SPACE'))
                self.alert_bmp.SetBitmap(error_bit.GetBitmap())
                self.name.SetBackgroundColour('#F9EDED')
                self.create.Disable()
                self.error_name = True
                return None

            elif name.strip(' ')[0] == '.':
                error_message = L('NEW_PRO_CONTAINS_POINT')
                self.error_name = True
            if '/' in name:
                error_message = L('NEW_PRO_CONTAINS_SLASH')
                self.error_name = True
            if len(name.strip(' ')) > 100:
                error_message = L('NEW_PRO_MAXIMUM_LENGTH')
                self.error_name = True
            if name in self.existing_names:
                error_message = L('NEW_PRO_EXISTING_NAME')
                self.error_name = True
            if name in self.hidden_names:
                error_message = L('NEW_PRO_HIDDEN_EXISTING_NAME')
                self.error_name = True

            if self.error_name:
                self.alert_text.SetLabel(error_message)
                self.alert_bmp.SetBitmap(error_bit.GetBitmap())
                self.name.SetBackgroundColour('#F9EDED')
                self.create.Disable()
                return None

            self.alert_text.SetLabel(L('NEW_PROJECT_ENTER_NAME'))
            self.alert_bmp.SetBitmap(execute_bit.GetBitmap())
            self.name.SetBackgroundColour('#FFFFFF')
            self.create.Enable()

    def on_change_formate(self, event):
        self.properties.set_file_format(self.rb.GetSelection())

    # --Funciones para agregar archivos -------------------------------------
    def OnButtonBrowse(self, event):

        last_path = self.properties.get_search_result()
        dlg = wx.FileDialog(self, message=L('ADD_FILE_DIALOG_TITLE'),
                            defaultDir=last_path,
                            wildcard=self.wildcard,
                            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            _ps = []
            if len(self.path_files) == 0:
                self.path_files = _ps = dlg.GetPaths()
            else:
                for p in dlg.GetPaths():
                    if not (p in self.path_files):
                        self.path_files.append(p)
                        _ps.append(p)

            for address in _ps:
                path, name = os.path.split(address)
                last_path = path
                self.dvlc.AppendItem([name, path])
        dlg.Destroy()
        self.properties.set_search_result(last_path)


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent, parent_object, size):
        wx.ListCtrl.__init__(self, parent, -1, size=size,
                             style=wx.LC_REPORT)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

        self.p = parent_object
        self.checked = []

    def OnCheckItem(self, index, flag):
        self.checked.append(index) if flag else self.checked.remove(index)
        self.p.ok.Enable() if len(self.checked) else self.p.ok.Disable()


class UnhideProject(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 550))

#         import py.una.pol.tavad.res.images as I
#         self.I = I

        self.InitUI()
        self.init_values()
        self.Centre()
        self.ShowModal()

    def InitUI(self):

        # ------ variables principales --------------------------------------
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(8, 5)

        # ------ Titulo de Proyecto Tava ------------------------------------
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(14)
        title1 = wx.StaticText(panel, label=L('NEW_PROJECT_TITLE'))
        title1.SetFont(font_title)

        exec_bmp = wx.StaticBitmap(panel)

        sizer.Add(title1, pos=(0, 0), flag=wx.LEFT | wx.TOP |
                  wx.ALIGN_LEFT, border=10)
        sizer.Add(exec_bmp, pos=(0, 4), flag=wx.ALIGN_CENTER)

        # ------ Texto Descriptivo que cambia --------------------------------
        des_box = wx.BoxSizer(wx.HORIZONTAL)

        font_description = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_description.SetPointSize(9)
        self.alert_text = wx.StaticText(panel)
        self.alert_text.SetFont(font_description)
        self.alert_text.SetLabel(L('UNHIDE_DESCRIPTION'))

        self.alert_bmp = wx.StaticBitmap(panel)
        self.alert_bmp.SetBitmap(execute_bit.GetBitmap())

        des_box.Add(self.alert_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        des_box.Add(self.alert_text, flag=wx.ALIGN_LEFT)

        sizer.Add(des_box, pos=(1, 0), span=(1, 3), flag=wx.LEFT, border=10)

        # ------ linea estática horizontal -----------------------------------
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 5), flag=wx.EXPAND |
                  wx.ALIGN_TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        # grilla de archivos (2)

        self.dvlc = CheckListCtrl(panel, self, size=(550, 298))

        # Establecemos las columnas con sus respectivos labels
        self.dvlc.InsertColumn(0, L('UNHIDE_COLUMN_NAME'), width=265)
        self.dvlc.InsertColumn(1, L('UNHIDE_COLUMN_HIDDEN'), width=150)
        self.dvlc.InsertColumn(2, L('UNHIDE_COLUMN_CREATION'), width=130)
        boxsizer.Add(self.dvlc, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=2)
        sizer.Add(boxsizer, pos=(3, 0), span=(1, 5), flag=wx.RIGHT |
                  wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        # ----- StaticBox agrupador -------------------------------------------
        sb = wx.StaticBox(panel, label=L('UNHIDE_BOX_LABEL'))
        static_box = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        select_all = wx.Button(panel, -1, L('UNHIDE_SELECT_ALL'))
        select_all.Bind(wx.EVT_BUTTON, self.on_all)
        unselect_all = wx.Button(panel, -1, L('UNHIDE_DESELECT_ALL'))
        unselect_all.Bind(wx.EVT_BUTTON, self.on_unall)
        hbox2.Add(select_all, 1, wx.ALL, 10)
        hbox2.Add(unselect_all, 1, wx.ALL, 10)
        static_box.Add(hbox2, 1, wx.EXPAND | wx.RIGHT, 250)
        sizer.Add(static_box, pos=(4, 0), span=(1, 5), flag=wx.RIGHT |
                  wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        # ---- BoxSizer para cancel, apply ------------------------------------
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        cancel = wx.Button(panel, -1, L('UNHIDE_CANCEL'))
        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.ok = wx.Button(panel, -1, L('UNHIDE_RESTORE'))
        self.ok.Bind(wx.EVT_BUTTON, self.on_unhide)
        self.ok.Disable()

        hbox3.Add(cancel, 1, wx.RIGHT, 20)
        hbox3.Add(self.ok)
        sizer.Add(hbox3, pos=(5, 0), span=(1, 5), flag=wx.RIGHT |
                  wx.LEFT | wx.ALIGN_RIGHT, border=10)
        # -------------------------------------------------------

        # ------ configuraciones Globales -----------------------------------
        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)
        panel.Bind(wx.EVT_CHAR, self.on_key_down)

    def on_cancel(self, event):
        self.parent.p_create = False
        self.Close()

    def on_key_down(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.Close()

    def on_unhide(self, event):
        ret = []
        for i in range(self.dvlc.GetItemCount()):
            if self.dvlc.IsChecked(i):
                ret.append(self.current[self.dvlc.GetItemText(i)])

        self.Hide()
        if len(ret):
            pub().sendMessage(T.UNHIDE_PROJECT, tuple(ret))
        self.Close()

    def init_values(self):
        self.current = ProjectM().for_unhide()
        for name, pro in self.current.items():
            index = self.dvlc.InsertStringItem(sys.maxint, name)
            self.dvlc.SetStringItem(index, 1, str(pro.creation))
            self.dvlc.SetStringItem(index, 2, str(pro.occultation))

    def on_all(self, event):
        for i in range(self.dvlc.GetItemCount()):
            self.dvlc.CheckItem(i)

    def on_unall(self, event):
        for i in range(self.dvlc.GetItemCount()):
            self.dvlc.CheckItem(i, False)


class ResultErrors(wx.Dialog):
    def __init__(self, parent, errores):
        wx.Dialog.__init__(self, parent, size=(400, 300))

        h_sizer = wx.BoxSizer()
        error_bmp = wx.StaticBitmap(self, -1, error_bit.GetBitmap())
        title = wx.StaticText(self, label=L('ERROR_REPORTING'))
        pts = title.GetFont().GetPointSize()
        title.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        h_sizer.Add(error_bmp)
        h_sizer.Add(title)

        st_line = wx.StaticLine(self)

        self.dvlc = dvlc = dv.DataViewListCtrl(self)
        dvlc.AppendTextColumn(L('FILE'), width=65)
        dvlc.AppendTextColumn(L('ERROR_MESSAGE'), width=100)

        for ers in errores:
            dvlc.AppendItem([ers.filename, ers.message])

        b_accep = wx.Button(self, label=L('OK'), size=(125, 32))
        b_accep.Bind(wx.EVT_BUTTON, self.on_accept)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(h_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT |
                  wx.RIGHT | wx.TOP, border=5)
        sizer.Add(st_line, flag=wx.EXPAND | wx.BOTTOM, border=5)
        sizer.Add(dvlc, 1, wx.EXPAND | wx.ALL, border=5)
        sizer.Add(b_accep, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)

        self.SetSizer(sizer)
        b_accep.SetFocus()

        self.Centre()
        self.ShowModal()

    def on_accept(self, event):
        self.Close()
