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
# Creado:  31/8/2016                                         ###
#                                                            ###
# ##############################################################
'''

from wx import GetTranslation as L
import wx
from wx.lib.itemspicker import IP_REMOVE_FROM_CHOICES, EVT_IP_SELECTION_CHANGED
from wx.lib.itemspicker import ItemsPicker, IP_SORT_CHOICES, IP_SORT_SELECTED

from imgs.iproject import execute_bit, error_bit
import wx.dataview as dv
import wx.wizard as wizmod


class ViewsTava(wizmod.Wizard):
    '''
    classdocs
    '''

    def __init__(self, parent, project):
        '''
        Constructor
        '''
        wizmod.Wizard.__init__(self, parent, -1, title=L('VIEW_TITLE_WIZARD'))
        self.parent = parent
        self.SetPageSize((600, 500))
        self.project = project
        self.pages = []
        self.result_nro_objetives = {}

        # create page for select results
        page_results = WizardPage(self)
        panel_result = PanelFirstPage(page_results, self.results_names(),
                                      self.views_names())
        page_results.add_stuff(panel_result)
        page_results.panel1 = panel_result
        self.add_page(page_results)
        self.page_1 = page_results

        # Add second page
        page_iteration = WizardPage(self)
        panel_iteration = PanelSecondtPage(page_iteration)
        page_iteration.add_stuff(panel_iteration)
        page_iteration.ldvPanel = panel_iteration
        self.add_page(page_iteration)
        self.page_2 = page_iteration

        self.Bind(wizmod.EVT_WIZARD_PAGE_CHANGED, self.on_page_changed)
        self.Bind(wizmod.EVT_WIZARD_FINISHED, self.on_finished)

        # self.FitToPage(self.page_1)
        self.RunWizard(self.pages[0])
        self.Destroy()

    def add_page(self, page):
        '''Add a wizard page to the list.'''
        if self.pages:
            previous_page = self.pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.pages.append(page)

    def on_page_changed(self, evt):

        forward_btn = self.FindWindowById(wx.ID_FORWARD)
        page = evt.GetPage()

        if evt.GetDirection():
            forward_btn.Disable()

            if page is self.pages[1]:

                # resultados seleccionados
                files = self.results_selected(self.page_1.ip.GetSelections())

                # opciones de iteraciones
                self.page_2.ldvPanel.dvc.ClearColumns()
                self.page_2.ldvPanel.init_dvc(files)
        else:
            forward_btn.Enable(True)

    def results_selected(self, results_names):
        ret = []
        for r in self.project.results:
            if r.name in results_names:
                ret.append(r)
        return ret

    def results_names(self):
        results_names = []
        for r in self.project.results:
            results_names.append(r.name)
            self.result_nro_objetives[r.name] = r.objectives
        return results_names

    def views_names(self):
        views_names = []
        for v in self.project.views:
            views_names.append(v.name)
        return views_names

    def enable_next(self, key=True):
        if key:
            self.FindWindowById(wx.ID_FORWARD).Enable()
        else:
            self.FindWindowById(wx.ID_FORWARD).Disable()

    def on_finished(self, evt):
        '''Finish button has been pressed.  Clean up and exit.'''

        self.parent.view_name = self.page_1.panel1.name.GetValue()
        for result in self.page_2.ldvPanel.data:
            if self.is_result_checked(result):
                self.parent.vews_results.append(result)

    def is_result_checked(self, result):
        for i in result.iterations:
            if i.check:
                return True
        return False


class WizardPage(wizmod.PyWizardPage):
    ''' '''
    def __init__(self, parent):
        wizmod.PyWizardPage.__init__(self, parent)

        self.next = self.prev = None

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, -1, L('VIEW_NEW_TITLE') + ' "' + 
                              parent.project.name + '"')
        title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer.AddWindow(title, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.sizer.AddWindow(wx.StaticLine(self, -1), 0, wx.EXPAND | 
                             wx.ALL, 5)

        self.SetSizer(self.sizer)

    def add_stuff(self, stuff):
        '''Add aditional widgets to the bottom of the page'''
        self.sizer.Add(stuff, 1, wx.EXPAND | wx.ALL, 5)

    def SetNext(self, next_):
        '''Set the next page'''
        self.next = next_

    def SetPrev(self, prev):
        '''Set the previous page'''
        self.prev = prev

    def GetNext(self):
        '''Return the next page'''
        return self.next

    def GetPrev(self):
        '''Return the previous page'''
        return self.prev


class PanelFirstPage(wx.Panel):
    def __init__(self, parent, results, views_names):
        wx.Panel.__init__(self, parent, -1, size=(300, 200))
        self.parent = parent
        self.error_name = True
        self.error_result = True
        self.views_names = views_names
        # self.I = I

        self.bmp_alert = wx.StaticBitmap(self)
        self.bmp_alert.SetBitmap(execute_bit.GetBitmap())
        font_description = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_description.SetPointSize(9)
        self.label_alert = wx.StaticText(self)
        self.label_alert.SetFont(font_description)
        self.label_alert.SetLabel(L('VIEW_ALERT_NAME'))

        label_name = wx.StaticText(self, label=L('VIEW_NAME'))
        self.name = wx.TextCtrl(self)

        label_results = wx.StaticText(self, label=L('VIEW_ALERT_RESULTS'))
        static_result = wx.StaticLine(self, -1)

        ip = ItemsPicker(self, -1, results, L('VIEW_OPTION_RESULTS'),
                         L('VIEW_RESULTS_SELECTED'), ipStyle=IP_SORT_CHOICES |
                         IP_SORT_SELECTED | IP_REMOVE_FROM_CHOICES)
        ip._source.SetMinSize((50, 100))
        parent.ip = ip

        # Create the sizers
        topSizer = wx.BoxSizer(wx.VERTICAL)
        alert_sizer = wx.BoxSizer(wx.HORIZONTAL)
        alert_sizer.Add(self.bmp_alert, flag=wx.ALIGN_LEFT)
        alert_sizer.Add(self.label_alert, flag=wx.ALIGN_LEFT)

        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(label_name, 0)
        name_sizer.Add(self.name, 1, wx.EXPAND)
        result_sizer = wx.BoxSizer(wx.VERTICAL)
        result_sizer.Add(label_results, 0, wx.ALIGN_CENTER)
        result_sizer.Add(static_result, 0, wx.ALIGN_CENTER | wx.EXPAND)
        topSizer.Add(alert_sizer, 0, wx.EXPAND)
        topSizer.Add(name_sizer, 0, wx.EXPAND)
        topSizer.Add(result_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        topSizer.Add(ip, 1, wx.EXPAND)
        self.SetSizer(topSizer)

        self.name.SetFocus()
        self.name.Bind(wx.EVT_KEY_UP, self.on_key_up)
        ip.Bind(EVT_IP_SELECTION_CHANGED, self.on_selected)
        self._disable()

    def on_selected(self, e):
        if e.GetItems():
            self.error_result = self.nro_objetives_verifict(e.GetItems())
        else:
            self.error_result = True
        self._disable()

    def on_key_up(self, e):
        name = self.name.GetValue()

        self.error_name = False
        error_message = ''

        if len(name) == 0:
            self.label_alert.SetLabel(L('NEW_PROJECT_ENTER_NAME'))
            self.bmp_alert.SetBitmap(execute_bit.GetBitmap())
            self.name.SetBackgroundColour('#FFFFFF')
            self.error_name = True
            self._disable()
            return None
        if len(name.strip(' ')) == 0:
            self.label_alert.SetLabel(L('NEW_PRO_BLANK_SPACE'))
            self.bmp_alert.SetBitmap(error_bit.GetBitmap())
            self.name.SetBackgroundColour('#F9EDED')
            self.error_name = True
            self._disable()
            return None

        if name.strip(' ')[0] == '.':
            error_message = L('NEW_PRO_CONTAINS_POINT')
            self.error_name = True
        if '/' in name:
            error_message = L('NEW_PRO_CONTAINS_SLASH')
            self.error_name = True
        if len(name.strip(' ')) > 100:
            error_message = L('NEW_PRO_MAXIMUM_LENGTH')
            self.error_name = True
        if name in self.views_names:
            error_message = L('NEW_PRO_EXISTING_NAME')
            self.error_name = True

        if self.error_name:
            self.label_alert.SetLabel(error_message)
            self.bmp_alert.SetBitmap(error_bit.GetBitmap())
            self.name.SetBackgroundColour('#F9EDED')
            self._disable()
            return None

        self.label_alert.SetLabel(L('NEW_PROJECT_ENTER_NAME'))
        self.bmp_alert.SetBitmap(execute_bit.GetBitmap())
        self.name.SetBackgroundColour('#FFFFFF')
        self.error_name = False
        self._disable()

    def _disable(self):
        if self.error_name or self.error_result:
            self.parent.GetParent().enable_next(False)
        else:
            self.parent.GetParent().enable_next()

    def nro_objetives_verifict(self, selecteds):
        _l = []
        for name in selecteds:
            _l.append(self.parent.GetParent().result_nro_objetives[name])
        if len(_l) == _l.count(_l[0]):
            return False
        return True


class PanelSecondtPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME)

        b_all = wx.Button(self, label=L('VIEW_ITE_CHECK_ALL'))
        b_unall = wx.Button(self, label=L('VIEW_ITE_UNCHECK_ALL'))

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

        b_sizer = wx.BoxSizer(wx.HORIZONTAL)
        b_sizer.Add(b_unall, flag=wx.RIGHT | wx.LEFT, border=10)
        b_sizer.Add(b_all, flag=wx.RIGHT | wx.LEFT, border=10)

        self.Sizer.Add(b_sizer, 0, wx.EXPAND)

        self.dvc.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.on_select)
        b_all.Bind(wx.EVT_BUTTON, self.on_all_selected)
        b_unall.Bind(wx.EVT_BUTTON, self.on_unall_selected)

        self.init_dvc(list())

    def on_all_selected(self, event):
        for result in self.data:
            for ite in result.iterations:
                ite.check = True
        self.Refresh()
        self.GetGrandParent().FindWindowById(wx.ID_FORWARD).Enable()

    def on_unall_selected(self, event):
        for result in self.data:
            for ite in result.iterations:
                ite.check = False
        self.Refresh()
        self.GetGrandParent().FindWindowById(wx.ID_FORWARD).Enable(False)

    def on_select(self, e):
        for result in self.data:
            for itr in result.iterations:
                if itr.check:
                    parent = self.GetGrandParent()
                    parent.FindWindowById(wx.ID_FORWARD).Enable()
                    return True
        self.GetGrandParent().FindWindowById(wx.ID_FORWARD).Enable(False)

    def init_dvc(self, results):

        data = dict()
        for r in results:
            v_result = ViewResult(r)
            for i in r.iterations:
                v_iteration = ViewIteration(i, r)
                v_result.iterations.append(v_iteration)
            data[r.name] = v_result

        data = data.values()

        # Create an instance of our model...
        self.model = MyTreeListModel(data)

        self.data = data
        # Tel the DVC to use the model
        self.dvc.AssociateModel(self.model)

        # Define the columns that we want in the view.  Notice the
        # parameter which tells the view which col in the data model to pull
        # values from for each view column.
        self.tr = tr = dv.DataViewTextRenderer()
        tr.EnableEllipsize()
        tr.SetAlignment(0)
        c0 = dv.DataViewColumn(L('VIEW_OPTION_RESULTS'),  # title
                               tr,  # renderer
                               0,  # data model column
                               width=200)
        self.dvc.AppendColumn(c0)

        c1 = self.dvc.AppendTextColumn(L('VIEW_ITERATION_F_R'), 1, width=200)
        c1.Alignment = wx.ALIGN_CENTRE

        self.dvc.AppendToggleColumn(L('VIEW_ITERATION_OPTION'), 2, width=20,
                                    mode=dv.DATAVIEW_CELL_ACTIVATABLE)

        # Set some additional attributes for all the columns
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        for node in self.model.getParentItem():
            self.dvc.Expand(node)


class MyTreeListModel(dv.PyDataViewModel):
    def __init__(self, data):
        dv.PyDataViewModel.__init__(self)
        self.data = data

        self.objmapper.UseWeakRefs(True)

    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        mapper = {0: 'string', 1: 'string', 2: 'bool'}
        return mapper[col]

    def GetChildren(self, parent, children):
        if not parent:
            for genre in self.data:
                children.append(self.ObjectToItem(genre))
            return len(self.data)

        node = self.ItemToObject(parent)
        if isinstance(node, ViewResult):
            for itr in node.iterations:
                children.append(self.ObjectToItem(itr))
            return len(node.iterations)
        return 0

    def IsContainer(self, item):
        if not item:
            return True

        node = self.ItemToObject(item)
        if isinstance(node, ViewResult):
            return True

        return False

    def GetParent(self, item):

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, ViewResult):
            return dv.NullDataViewItem
        elif isinstance(node, ViewIteration):
            for rf in self.data:
                if rf.name == node.result_file:
                    return self.ObjectToItem(rf)

    def GetValue(self, item, col):
        node = self.ItemToObject(item)

        if isinstance(node, ViewResult):
            mapper = {0: node.name, 1: "", 2: False}
            return mapper[col]

        elif isinstance(node, ViewIteration):
            mapper = {0: "", 1: node.label, 2: node.check}
            return mapper[col]

        else:
            raise RuntimeError("unknown node type")

    def GetAttr(self, item, col, attr):
        node = self.ItemToObject(item)
        if isinstance(node, ViewResult):
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def SetValue(self, value, item, col):
        node = self.ItemToObject(item)
        if isinstance(node, ViewIteration):
            if col == 2:
                node.check = value

    def getParentItem(self):
        itemParent = []
        for node in self.data:
            if isinstance(node, ViewResult):
                itemParent.append(self.ObjectToItem(node))
        return itemParent


class ViewResult(object):
    def __init__(self, result):
        self.name = result.name
        self.result = result
        self.iterations = []

    def __repr__(self):
        return 'ViewResult: ' + self.name


class ViewIteration(object):
    def __init__(self, iteration, result):
        self.label = str(iteration.number)
        self.check = False
        self.result_file = result.name
        self.iteration = iteration

    def __repr__(self):
        return 'ViewIteration %s-%s' % (self.label, self.result_file)
