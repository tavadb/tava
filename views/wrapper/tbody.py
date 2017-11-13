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
from wx.lib.agw import customtreectrl as CT, aui
from wx.lib.pubsub import Publisher as pub

from bd.entity import Project, Result, View
from imgs.itree import iopen, iopened, iclose, \
    iview_package_open, iview_package_close, iview_pack
from languages import topic as T
from presenters.ptree import TTreeP, PackageFile, PackageView
from views.wrapper.vmenu.vtree import MenuVista, MenuPackageView, MenuResult,\
    MenuResultFile
from views.wrapper.wraview.mainview import ViewMainPanel


KURI_AUI_NB_STYLE = aui.AUI_NB_TOP | aui.AUI_NB_TAB_SPLIT | \
    aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS |\
    aui.AUI_NB_CLOSE_BUTTON | aui.AUI_NB_DRAW_DND_TAB


class CentralPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.v_setting()

        pub().subscribe(self.show_view, T.SHOW_SELECTED_VIEW)
        pub().subscribe(self.pre_delete_page, T.PRE_DELETE_VIEW)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.v_content()

    def v_setting(self):
        self.SetBackgroundColour("#3B598D")

    def v_content(self):

        self.instancias_page = []
        self.instancias_view = []

        self.nb_main = aui.AuiNotebook(self)
        ar = aui.ChromeTabArt()
        ar.SetAGWFlags(aui.AUI_NB_TAB_SPLIT)
        self.nb_main.SetArtProvider(ar)
        # self.nb_main.SetAGWWindowStyleFlag(KURI_AUI_NB_STYLE)
        self.nb_main.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        # self.nb_main.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_change)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.nb_main, 1,
                       wx.LEFT | wx.TOP | wx.EXPAND | wx.ALL, 1)
        self.SetSizer(self.sizer)
        self.Fit()

    def show_view(self, message):
        view = message.data

        if view.id in self.instancias_view:
            id_page = self.instancias_view.index(view.id)
            self.nb_main.SetSelection(id_page)
        else:
            self.nb_main.AddPage(ViewMainPanel(self.nb_main, view),
                                 view.name, True)

            # --- se guardan las instancias
            self.instancias_page.append(len(self.instancias_page))
            self.instancias_view.append(view.id)

    def on_close(self, event):
        page = self.nb_main.GetCurrentPage()
        if page is not None:
            id_page = self.nb_main.GetPageIndex(page)
            self.instancias_page.remove(self.instancias_page[id_page])
            self.instancias_view.remove(self.instancias_view[id_page])
            if id_page != len(self.instancias_page):
                p = self.instancias_page
                self.instancias_page = p[:id_page] + [i-1 for i in p[id_page:]]

    def pre_delete_page(self, message):
        view_id = message.data.id
        if view_id in self.instancias_view:
            self.nb_main.RemovePage(self.instancias_view.index(view_id))
        pub().sendMessage(T.DELETE_VIEW, message.data)

    def on_change(self, event):
        print 'Change tab'


class TTree(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent)

        self.v_setting()
        self.v_content()

        self.ppr = TTreeP(self)
        self.c_item = None
        self.c_data = None

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_selected)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_dclick)
        self.Bind(wx.EVT_RIGHT_UP, self.on_contex)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.on_expanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.on_collapsed)

    def v_setting(self):
        # self.SetBackgroundColour("red")
        self.SetSize(wx.Size(220, -1))
        self.SetAGWWindowStyleFlag(CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

    def v_content(self):

        img_list = wx.ImageList(16, 16)
        img_list.Add(iopen.GetBitmap())
        img_list.Add(iopened.GetBitmap())
        img_list.Add(iclose.GetBitmap())

        img_list.Add(iview_package_close.GetBitmap())
        img_list.Add(iview_package_open.GetBitmap())

        img_list.Add(iview_pack.GetBitmap())

        self.AssignImageList(img_list)

        self.root = self.AddRoot("TAVA TREE PROJECT", 0)

    # --- node open project
    def add_open_project(self, project):
        project_item = self.AppendItem(self.root, project.name)
        return self.update_open_project(project_item, project)

    def update_open_project(self, project_item, project):
        self.SetItemPyData(project_item, [project, project.proj_open])
        self.SetItemImage(project_item, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 1, wx.TreeItemIcon_Expanded)
        self.SetItemTextColour(project_item, '#000000')
        self._expanded(project_item, project.proj_open)
        return project_item

    # --- node closed project
    def add_closed_project(self, project):
        project_item = self.AppendItem(self.root, project.name)
        return self.update_close_project(project_item, project)

    def update_close_project(self, project_item, project):
        self.SetItemPyData(project_item, [project, False])
        self.SetItemImage(project_item, 2, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 2, wx.TreeItemIcon_Expanded)
        self.SetItemTextColour(project_item, '#AABBCC')
        return project_item

    # --- node files package
    def add_package_files(self, item_p, pack_file):
        item_file_package = self.AppendItem(item_p, self._package_file_name())
        self.SetItemPyData(item_file_package, [pack_file, pack_file.state])
        self.SetItemImage(item_file_package, 3, wx.TreeItemIcon_Normal)
        self.SetItemImage(item_file_package, 4, wx.TreeItemIcon_Expanded)
        self._expanded(item_file_package, pack_file.state)
        return item_file_package

    # --- node views package
    def add_package_views(self, item_p, pack_view):
        item_views_package = self.AppendItem(item_p, self._package_view_name())
        self.SetItemPyData(item_views_package, [pack_view, pack_view.state])
        self.SetItemImage(item_views_package, 5, wx.TreeItemIcon_Normal)
        self._expanded(item_views_package, pack_view.state)
        return item_views_package

    # --- node results
    def add_results(self, item_pack, result):
        item_result = self.AppendItem(item_pack, result.name)
        self.SetItemPyData(item_result, [result, True])
        return item_result

    # --- node views
    def add_views(self, item_pack, view):
        item_view = self.AppendItem(item_pack, view.name)
        self.SetItemPyData(item_view, [view, True])
        return item_view

    # --- node views - result
    def add_result_view(self, item_view, name):
        item_view = self.AppendItem(item_view, name)
        self.EnableItem(item_view, False)
        return item_view

    def grandfather(self, item):
        father = self.GetItemParent(item)
        return self.GetItemParent(father)

    def sort_tree(self, item=None):
        if item is None:
            self.SortChildren(self.root)
        else:
            self.SortChildren(item)

    def pre_hide_project(self, name):
        result = wx.MessageBox(L('HIDE_PROJECT_BOX') + '\n\t\t\t\t" ' +
                               name + ' "', L('HIDE_PROJECT_TITLE'),
                               style=wx.CENTER | wx.ICON_WARNING |
                               wx.YES_NO | wx.NO_DEFAULT)
        if result == wx.YES:
            return True
        return False

    def on_expanded(self, event):
        data = event.GetItem().GetData()
        data[1] = True

    def on_collapsed(self, event):
        data = event.GetItem().GetData()
        data[1] = False

    def pre_delete_project(self, name):
        result = wx.MessageBox(L('DELETE_PROJECT_BOX') + '\n\t\t\t\t" ' +
                               name + ' "', L('DELETE_PROJECT_TITLE'),
                               style=wx.CENTER | wx.ICON_WARNING |
                               wx.YES_NO | wx.NO_DEFAULT)
        if result == wx.YES:
            return True
        return False

    # ------------------------------------------------------------------
    # --------------- metodos privados ---------------------------------
    # ------------------------------------------------------------------

    # -- selected item
    def on_selected(self, event):
        self.c_item = event.GetItem()
        self.c_data = self.c_item.GetData()
        if self.c_data is not None:
            self.ppr.do_selected(self.c_data[0], self.c_item)
            pass

    # --- selected contex menu
    def on_dclick(self, event):
        if self.c_data is None:
            return None
        data = self.c_data[0]
        if isinstance(data, Project):
            pass
        elif isinstance(data, PackageFile):
            pass
        elif isinstance(data, PackageView):
            pass
        elif isinstance(data, Result):
            pass
        elif isinstance(data, View):
            pub().sendMessage(T.SHOW_SELECTED_VIEW, data)

    # --- selected contex menu
    def on_contex(self, event):
        data = self.c_data[0]
        if isinstance(data, Project):
            pass
#             print 'Click derecho en Proyecto'
            # menu_p = MenuP(self, data)
            # self.PopupMenu(menu_p)
        elif isinstance(data, PackageFile):
            menu_p = MenuResult(self, data.project)
            self.PopupMenu(menu_p)
            # print 'Click derecho en Paquete Resultado'
        elif isinstance(data, PackageView):
            # print 'Click derecho en Paquete de Vista'
            menu_p = MenuPackageView(self, data.project)
            self.PopupMenu(menu_p)
        elif isinstance(data, Result):
            # print 'Click derecho en Result'
            menu_p = MenuResultFile(self, data)
            self.PopupMenu(menu_p)
        elif isinstance(data, View):
            menu_p = MenuVista(self, data)
            self.PopupMenu(menu_p)
#             print 'Click derecho en Vista'
#         else:
#             print 'ninguno de los anteriores'

    def _expanded(self, item, expand=True):
        if expand:
            item.Expand()
        else:
            item.Collapse()

    def delete_item_selected(self):
        _item = self.c_item.GetParent()
        self.Delete(self.c_item)
        self.c_item = _item
        self.c_data = _item.GetData()
        self.SelectItem(self.c_item)

    def _package_file_name(self):
        return L('PACKAGE_FILES_NAME')

    def _package_view_name(self):
        return L('PACKAGE_VIEWS_NAME')
