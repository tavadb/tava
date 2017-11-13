#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)      ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  26/8/2016                                          ###
#                                                            ###
# ##############################################################
'''

from wx import GetTranslation as L
import wx
from wx.lib.agw import aui
from wx.lib.agw import pyprogress as PP
from wx.lib.pubsub import Publisher as pub

from bd import entity
from imgs.itree import explorer
from imgs.prin import shortcut, splash
from languages import topic as T
from languages.i18n import I18nLocale
from presenters.pmain import MainFrameP
from resources.properties_helper import PropertiesHelper
from views.wrapper.tbody import TTree, CentralPanel
from views.wrapper.tmenubar import TMenuBar
from views.wrapper.ttoolbar import TToolBar
from views.wrapper.vdialog.vproject import NewProject, UnhideProject, \
    ResultErrors
from views.wrapper.vdialog.vview import ViewsTava
import EnhancedStatusBar as ESB


class MainFrame(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)

        self.v_setting()

        # --- vistas
        pub().subscribe(self.new_view, T.CREATE_VIEW)
        pub().subscribe(self.delete_view, T.DELETE_VIEW)

        # ---- results
        pub().subscribe(self.new_results, T.NEW_RESULTS)
        pub().subscribe(self.delete_result, T.DELETE_RESULT)
        pub().subscribe(self.change_name_objectives, T.CHANGE_RESULT)
        

        # ---- project
        pub().subscribe(self.unhide_project, T.PREUNHIDE_PROJECT)

        # ---- statusbar
        pub().subscribe(self.start_busy, T.START_BUSY)
        pub().subscribe(self.stop_busy, T.STOP_BUSY)

        # ---- properties helper
        self.properties = PropertiesHelper()

        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.v_content()

        self.ppr = MainFrameP(self)

        self.Bind(wx.EVT_CLOSE, self.on_close_tava)

    def on_close_tava(self, event):

        result = wx.MessageBox(L('EXIT_TAVA'), L('EXIT_TAVA_HEADER'),
                               style=wx.CENTER | wx.ICON_QUESTION |
                               wx.YES_NO | wx.NO_DEFAULT)
        if result == wx.YES:
            self.tree.ppr.do_exit()
            self.Destroy()
        return False

    def on_exit(self, event):
        self.tree.ppr.do_exit()
        self.Destroy()

    def v_setting(self):
        self.SetTitle("FPUNA: Tava")
        self.SetSize(wx.Size(960, 540))
        self.SetBackgroundColour("#F5D0A9")
        self.SetMinSize((660, 480))
        self.SetIcon(shortcut.GetIcon())
        self.Center(wx.BOTH)

    def v_content(self):

        # configuración de lenguajes
        self.i18n = I18nLocale(self.properties.get_language())

        # aui que manejará los paneles principales
        self._mgr = aui.AuiManager(self, aui.AUI_MGR_ANIMATE_FRAMES)

        # add Menu Bar
        self.menu_bar = TMenuBar(self)
        self.SetMenuBar(self.menu_bar)

        self.set_status_bar()

        self.build_panels()

        self.Bind(wx.EVT_SIZE, self.on_resize_window)

    def set_status_bar(self):
        self.statusbar = ESB.EnhancedStatusBar(self, -1)
        self.statusbar.SetFieldsCount(2)
        self.SetStatusBar(self.statusbar)
        self.statusbar.SetStatusWidths([-1, 150])
        self.statusBarText = wx.StaticText(self.statusbar, -1, "   " +
                                   L('STATUS_WELCOME_MSG'))
        self.statusbar.AddWidget(self.statusBarText,
                                 horizontalalignment=ESB.ESB_ALIGN_LEFT, pos=0)
        self.prog = wx.Gauge(self.statusbar, size=(125, 10))
        self.statusbar.AddWidget(self.prog, pos=1)
        self.prog.Hide()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_pulse, self.timer)

    def on_pulse(self, event):
        self.prog.Pulse()

    def start_busy(self, msg):
        self.timer.Start(100)
        self.prog.Show()

    def stop_busy(self, msg):
        self.timer.Stop()
        self.prog.Hide()

    def on_resize_window(self, event):
        self.prog = wx.Gauge(self.statusbar, size=(125, 10))
        self.statusbar.AddWidget(self.prog, pos=1)
        self.prog.Hide()
        event.Skip()

    def build_panels(self):

        # ---- toolbar de la aplicación
        self.ttoolbar = TToolBar(self)
        self._mgr.AddPane(self.ttoolbar, aui.AuiPaneInfo().Name("tb1").
                          Caption("Big Toolbar").ToolbarPane().Top())

        # ---- tree de proyectos
        self.tree = TTree(self)
        self._mgr.AddPane(self.tree,
                          aui.AuiPaneInfo().Name("tree_pane").
                          Icon(explorer.GetBitmap()).
                          Caption(L('PROJECT_EXPLORER')).
                          Left().Layer(1).Position(1).CloseButton(False).
                          MaximizeButton(True).MinimizeButton(True).
                          Floatable(False))

        # Panel central
        self._mgr.AddPane(CentralPanel(self), aui.AuiPaneInfo().
                          Name("space_work_pane").CenterPane())
        self._mgr.Update()

    def change_language(self, language):

        if not self.i18n.isEnUsLanguage() and language == 'en':
            self.i18n.OnEnUs()
            self.update_language()
            pub().sendMessage(T.LANGUAGE_CHANGED)
            self.properties.set_language('en')

        if not self.i18n.isEsPyLanguage() and language == 'es':
            self.i18n.OnEsPy()
            self.update_language()
            pub().sendMessage(T.LANGUAGE_CHANGED)
            self.properties.set_language('es')

    def update_language(self):
        self._mgr.GetPaneByName("tree_pane").Caption(L('PROJECT_EXPLORER'))
        self._mgr.RefreshCaptions()
        self.menu_bar.SetLabelsLanguages()
        self.ttoolbar.SetLabelsLanguages()
        self.statusBarText.SetLabel("   " + L('STATUS_WELCOME_MSG'))

    # ------------- funciones logicas ---------------------

    def new_project(self):
        self.p_name = ''
        self.p_path_files = []
        self.p_formate = 10
        self.p_create = False
        self.p_sep = ','

        NewProject(self, self.properties)
        if self.p_create:
            project = self.ppr.add_project(self.p_name)

            if self.p_path_files != []:
                style = wx.PD_APP_MODAL
                style |= wx.PD_CAN_ABORT

                dlg = PP.PyProgress(self, -1, L('MSG_PRO_HEADER_TITLE'),
                                    "                              :)",
                                    agwStyle=style)
                _, errs = self.ppr.add_res(project, self.p_path_files,
                                           self.p_formate, self.p_sep, dlg)
                dlg.Close()
                dlg.Destroy()

                # ---- informe de archivos con errores
                if errs != []:
                    ResultErrors(self, errs)

                wx.SafeYield()
                wx.GetApp().GetTopWindow().Raise()

            pub().sendMessage(T.ADD_PROJECT_IN_TREE, project)

    def new_results(self, message):
        self.p_project = message.data
        self.p_path_files = []
        self.p_formate = 10
        self.p_create = False
        self.p_sep = ','

        NewProject(self, self.properties, True)
        if self.p_create:

            style = wx.PD_APP_MODAL
            style |= wx.PD_CAN_ABORT
            dlg = PP.PyProgress(self, -1, L('MSG_PRO_HEADER_TITLE'),
                                "                              :)",
                                agwStyle=style)

            res, errs = self.ppr.add_res(self.p_project, self.p_path_files,
                                         self.p_formate, self.p_sep, dlg)
            dlg.Close()
            dlg.Destroy()

            # ---- informe de archivos con errores
            if errs != []:
                ResultErrors(self, errs)

            pub().sendMessage(T.ADD_RESULTS_IN_TREE, res)

            wx.SafeYield()
            wx.GetApp().GetTopWindow().Raise()

    def delete_result(self, message):

        if self.ppr.contain_view(message.data.id):
            # ---- no se puede eliminar resultado, utilizado en vista
            dlg = wx.MessageDialog(self, L('RESULT_NOT_DELETE'),
                                   L('RESULT_NOT_DELETE_HEADER'),
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            # --- elimina de la bd y envía mensaje de eliminación
            self.ppr.delete_result(message.data)
            pub().sendMessage(T.DELETE_RESULT_TREE)

    def change_name_objectives(self, message):

        dlg = wx.TextEntryDialog(
                self, L('RESULT_CHANGE_NAME_ST'),
                L('RESULT_CHANGE_NAME_T'), 'Python')
        delimitadores = self.contar_coma(message.data.name_objectives)
        dlg.SetValue(message.data.name_objectives)

        if dlg.ShowModal() == wx.ID_OK:
            if delimitadores == self.contar_coma(dlg.GetValue()):
                message.data.name_objectives = dlg.GetValue()
                self.ppr.update_result(message.data)

        dlg.Destroy()

    def new_view(self, message):
        project = message.data
        self.view_name = ''
        self.vews_results = []

        ViewsTava(self, project)
        if self.vews_results:
            view = self.ppr.add_views(self.view_name,
                                      self.vews_results, project)
            pub().sendMessage(T.ADD_VIEW_IN_TREE, view)

    def delete_view(self, message):
        self.ppr.delete_view(message.data)
        pub().sendMessage(T.DELETE_VIEW_TREE)

    def unhide_project(self, message):
        UnhideProject(self)
        
    def contar_coma(self, cadena):
        contador = 0
        for letra in cadena:
            if letra == "A":
                contador += 1
        return(contador)


class SplashFrame(wx.SplashScreen):

    def __init__(self):
        wx.SplashScreen.__init__(self, splash.GetBitmap(),
                                 wx.SPLASH_CENTRE_ON_SCREEN |
                                 wx.SPLASH_TIMEOUT, 5000, None, -1)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(2000, self.ShowMain)

    def OnClose(self, evt):
        evt.Skip()
        self.Hide()
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        entity.createDB()
        frame = MainFrame(None)
        frame.Center(wx.BOTH)
        frame.Show()

        if self.fc.IsRunning():
            self.Raise()
        wx.SafeYield()
        wx.GetApp().GetTopWindow().Raise()
