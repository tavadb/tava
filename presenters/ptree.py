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
# Creado:  30/8/2016                                          ###
#                                                            ###
# ##############################################################
'''
from wx.lib.pubsub import Publisher as pub

from bd.entity import Project
from languages import topic as T
from models.mproject import ProjectM as pm


class TTreeP(object):
    '''
    classdocs
    '''

    def __init__(self, iview):
        '''
        Constructor
        '''
        # ---- projectos
        pub().subscribe(self.add_project_in_tree, T.ADD_PROJECT_IN_TREE)
        pub().subscribe(self.pre_close, T.CLOSE_PROJECT)
        pub().subscribe(self.pre_open, T.OPEN_PROJECT)
        pub().subscribe(self.pre_hide, T.HIDE_PROJECT)
        pub().subscribe(self.pre_unhide, T.UNHIDE_PROJECT)
        pub.subscribe(self.pre_delete, T.DELETE_PROJECT)
        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        # ---- vistas
        pub().subscribe(self.add_view_in_tree, T.ADD_VIEW_IN_TREE)
        pub().subscribe(self.delete_view, T.DELETE_VIEW_TREE)

        # --- results
        pub().subscribe(self.add_results_in_tree, T.ADD_RESULTS_IN_TREE)
        pub().subscribe(self.delete_result, T.DELETE_RESULT_TREE)

        self.iview = iview
        self.init_tree()

        # ---- variables de estado
        self.last_sate_project = None
        self.less_project = False

    def init_tree(self):

        # proyectos abiertos
        for project in pm().state_open():
            item_p = self.iview.add_open_project(project)
            self.add_packages_item(item_p, project)

        # proyectos cerrados
        for project in pm().state_close():
            self.iview.add_closed_project(project)

    def add_packages_item(self, item_project, project):

        # Agregar los archivos resultados del proyecto
        pfile = PackageFile(project.pack_file, project)
        pack_file = self.iview.add_package_files(item_project, pfile)

        for r in project.results:
            self.iview.add_results(pack_file, r)

        # Agregar vistas del proyecto
        pview = PackageView(project.pack_view, project)
        pack_view = self.iview.add_package_views(item_project, pview)

        for v in project.views:
            item = self.iview.add_views(pack_view, v)
            for i, vr in enumerate(v.results):
                name = 'r' + str(i+1) + ' - ' + vr.result.name
                self.iview.add_result_view(item, name)

        return pack_file, pack_view

    # --- add new project in tree ------------------------------------
    def add_project_in_tree(self, message):
        project = message.data
        # self.init_vars()
        # pub().sendMessage(T.TYPE_CHANGED_SELECTED_PROJECT, 4)

        item_p = self.iview.add_open_project(project)
        self.add_packages_item(item_p, project)
        self.iview.ExpandAllChildren(item_p)

    def add_view_in_tree(self, message):
        new_view = message.data
        item = self.iview.add_views(self.iview.c_item, new_view)
        for i, vr in enumerate(new_view.results):
            name = 'r' + str(i+1) + ' - ' + vr.result.name
            self.iview.add_result_view(item, name)
        self.iview.Expand(self.iview.c_item)
        self.iview.Expand(item)
        self.iview.SelectItem(item)

    def add_results_in_tree(self, message):
        for r in message.data:
            self.iview.add_results(self.iview.c_item, r)
        self.iview.Expand(self.iview.c_item)

    def delete_result(self, message):
        self.iview.delete_item_selected()

    def delete_view(self, message):
        self.iview.delete_item_selected()

    # ---- selected item
    def do_selected(self, data, item):

        if isinstance(data, Project):
            self.last_sate_project = data.state
            self.less_project = True
            pub().sendMessage(T.TYPE_CHANGED_SELECTED_PROJECT, data.state)
        elif self.less_project:
            self.less_project = False
            pub().sendMessage(T.TYPE_CHANGED_UNSELECTED_PROJECT)

    # --- close project ---------------------------------------------
    def pre_close(self, message):
        self.do_close(self.iview.c_data[0], self.iview.c_item)

    def do_close(self, project, item):
        proj_open = item.GetData()[1]
        chil_p = item.GetChildren()
        pack_fil = chil_p[0].GetData()[1]
        pack_vie = chil_p[1].GetData()[1]

        project = pm().update_by_close(project, proj_open, pack_fil, pack_vie)

        item = self.iview.update_close_project(item, project)
        self.iview.DeleteChildren(item)
        self.iview.sort_tree()
        self.pos_close(project)

    def pos_close(self, project):
        self.less_project = False
        pub().sendMessage(T.TYPE_CHANGED_UNSELECTED_PROJECT)

    # --- open project
    def pre_open(self, message):
        self.do_open(self.iview.c_data[0], self.iview.c_item)

    def do_open(self, project, item):
        project = pm().update_by_open(project)
        item = self.iview.update_open_project(item, project)
        self.add_packages_item(item, project)
        self.iview.sort_tree()
        self.pos_open(project)

    def pos_open(self, project):
        self.less_project = False
        pub().sendMessage(T.TYPE_CHANGED_UNSELECTED_PROJECT)

    # --- hide project
    def pre_hide(self, message):
        if self.iview.pre_hide_project(self.iview.c_data[0].name):
            self.do_hide(self.iview.c_data[0], self.iview.c_item)

    def do_hide(self, project, item):
        pm().update_by_hide(project)
        self.iview.Delete(item)

    def pos_hide(self):
        self.less_project = False
        pub().sendMessage(T.TYPE_CHANGED_UNSELECTED_PROJECT)

    # --- unhide project
    def pre_unhide(self, message):
        self.do_unhide(message.data)

    def do_unhide(self, projects):
        for pro in projects:
            pro = pm().update_by_unhide(pro)
            item_p = self.iview.add_open_project(pro)
            self.add_packages_item(item_p, pro)
            self.iview.Expand(item_p)
        self.iview.sort_tree()

    def pos_unhide(self):
        self.init_vars()
        pub().sendMessage(T.TYPE_CHANGED_UNSELECTED_PROJECT)

    # --- delete project ---------------------------------------------
    def pre_delete(self, message):
        if self.iview.pre_delete_project(self.iview.c_data[0].name):
            self.do_delete(self.iview.c_data[0])

    def do_delete(self, project):
        pm().delete(project)
        self.iview.Delete(self.iview.c_item)
        self.pos_delete()

    def pos_delete(self):
        pub.sendMessage(T.TYPE_CHANGED_UNSELECTED_PROJECT)

    # --- exit app ---------------------------------------------
    def do_exit(self):
        for item_p in self.iview.root.GetChildren():
            data_item = item_p.GetData()
            p = data_item[0]
            pp = data_item[1]

            chil_p = item_p.GetChildren()
            if len(chil_p) > 0:
                pf = chil_p[0].GetData()[1]
                pv = chil_p[1].GetData()[1]

                if p.proj_open != pp or p.pack_file != pf or p.pack_view != pv:
                    p.proj_open = pp
                    p.pack_file = pf
                    p.pack_view = pv
                    pm().update(p)

    def update_language(self, message):
        '''
        Actualiza nombres de módulos y paquetes del tree principal cuando se
        cambia el lenguaje.

        :param Message: Mensaje conteniendo el topic.
        '''
        for item_p in self.iview.root.GetChildren():
            for item_module in item_p.GetChildren():
                m_data = item_module.GetData()
                if isinstance(m_data[0], PackageFile):
                    item_module.SetText(self.iview._package_file_name())
                else:
                    item_module.SetText(self.iview._package_view_name())
                self.iview.RefreshSubtree(item_module)
            self.iview.RefreshSubtree(item_p)


class PackageFile():
    def __init__(self, state, project):
        self.state = state
        self.project = project
    pass


class PackageView():
    def __init__(self, state, project):
        self.state = state
        self.project = project
    pass
