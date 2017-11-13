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
# Creado:  27/8/2016                                         ###
#                                                            ###
# ##############################################################
'''

from wx import GetTranslation as L
import wx

from imgs.prin import shortcut


class TMenuBar(wx.MenuBar):

    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent

        # ---- Menu File ---------------------
        file_menu = wx.Menu()

        # menu items - menu file
        self.exit = wx.MenuItem(file_menu, wx.ID_ANY, ' ')

        # add menu to item
        file_menu.AppendItem(self.exit)

        # add events
        file_menu.Bind(wx.EVT_MENU, parent.on_exit, self.exit)

        # ---- Menu Languages ---------------
        language_menu = wx.Menu()
        self.es_py_language = wx.MenuItem(language_menu, wx.ID_ANY, ' ')
        self.en_us_language = wx.MenuItem(language_menu, wx.ID_ANY, ' ')

        language_menu.AppendItem(self.es_py_language)
        language_menu.AppendItem(self.en_us_language)

        language_menu.Bind(wx.EVT_MENU, self.OnEnUsSelect, self.en_us_language)
        language_menu.Bind(wx.EVT_MENU, self.OnEsPySelect, self.es_py_language)

        # ---- Menu Help --------------------
        help_menu = wx.Menu()
        self.about = wx.MenuItem(help_menu, wx.ID_ANY, ' ')
        help_menu.AppendItem(self.about)
        help_menu.Bind(wx.EVT_MENU, self.OnAboutBox, self.about)

        # ---- menus ------------------------
        self.Append(file_menu, ' ')
        self.Append(language_menu, ' ')
        self.Append(help_menu, ' ')

        self.SetLabelsLanguages()

    def SetLabelsLanguages(self):
        # ---- Menu File ---------------------
        self.SetMenuLabel(0, L('MENU_BAR_FILE'))
        self.exit.SetText('&' + L('MENU_BAR_EXIT') + '\tCtrl+Q')

        # ---- Menu Languages ----------------
        self.SetMenuLabel(1, L('MENU_BAR_LANGUAGE'))
        self.en_us_language.SetText(L('MENU_BAR_EN_US_LANGUAGE'))
        self.es_py_language.SetText(L('MENU_BAR_ES_PY_LANGUAGE'))

        # ---- Menu Help --------------------
        self.SetMenuLabel(2, L('MENU_BAR_HELP'))
        self.about.SetText(L('MENU_BAR_ABOUT'))

    def OnEnUsSelect(self, e):
        self.parent.change_language('en')

    def OnEsPySelect(self, e):
        self.parent.change_language('es')

    def OnAboutBox(self, e):
        '''
        Método que inicializa la clase que representa al panel "Acerca de".
        :param e: evento de selección de Menú.
        '''
        AboutDialog()


class AboutDialog(wx.AboutDialogInfo):
    '''
    Clase que representa a la ventana que despliega información acerca de
    detalles del programa.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(AboutDialog, self).__init__()

        description = L('MENU_ABOUT_DESCRIPTION')
        licence = L('MENU_ABOUT_LICENSE')

        self.SetIcon(shortcut.GetIcon())
        self.SetName('Tava')
        self.SetVersion('1.0')
        self.SetDescription(description)
        self.SetCopyright('(C) 2015 - 2016 fp-una')
        self.SetWebSite('http://www.pol.una.py')
        self.SetLicence(licence)
        self.AddDeveloper('Abrahan Fretes')
        self.AddDeveloper('Arsenio Ferreira')
        self.AddDocWriter('Arsenio Ferreira')
        self.AddDocWriter('Abrahan Fretes')
        self.AddTranslator('Arsenio Ferreira')
        self.AddTranslator('Abrahan Fretes')

        wx.AboutBox(self)
