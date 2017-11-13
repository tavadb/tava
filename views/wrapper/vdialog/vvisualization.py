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
# Creado:  01/10/2016                                        ###
#                                                            ###
# ##############################################################
'''
import wx
from wx import GetTranslation as L
from wx.lib.pubsub import Publisher as pub
from languages import topic as T

V_M_CLUSTER = 0
V_M_SUMMARY = 1
V_M_CLUSTER_SUMMARY = 2


class ClusterConfig(wx.Dialog):
    """
    Vista de configuración para la visualizacion de clusters.
    """

    def __init__(self, parent):
        _title = L('CLUSTER_CONFIG')
        wx.Dialog.__init__(self, parent, title=_title, size=(400, 560))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        sboxs_vm = self.set_visualization_mode()

        sbuttons = self.set_buttons()

        line = self.get_line()

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_vm, 0, wx.EXPAND | wx.ALL, 7)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(msizer, 0, wx.EXPAND)
        _style = wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP
        sizer.Add(line, 0, _style, 5)
        sizer.Add(sbuttons, flag=wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM,
                  border=10)

        self.SetSizer(sizer)
        self.Show()

    def set_visualization_mode(self):
        self.sbox_mv = wx.StaticBox(self, -1, L('DISPLAY_MODE'))
        sboxs_mv = wx.StaticBoxSizer(self.sbox_mv, wx.HORIZONTAL)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Choicebook(p, -1)

        # add the pages to the notebook with the label to show on the tab
        self.page_cluster = ClusterPage(nb, self)
        nb.AddPage(self.page_cluster, "Clusters")
        self.page_resumes = SummaryPage(nb, self)
        nb.AddPage(self.page_resumes, L('SUMMARIES'))
        self.page_cluster_sumary = ClusterSummaryPage(nb, self)
        nb.AddPage(self.page_cluster_sumary, L('CLUSTERS_AND_SUMMARIES'))

        nb.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_page_changed)
        self.nb = nb

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND | wx.EXPAND, 5)
        p.SetSizer(sizer)

        sboxs_mv.Add(p, 1, wx.ALL | wx.EXPAND, 5)
        return sboxs_mv

    def on_page_changed(self, e):
        selection = e.GetSelection()
        self.GetParent().visualization_mode = selection
        e.Skip()

    def set_buttons(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        ok_button = wx.Button(self, label=L('OK'))
        ok_button.SetDefault()
        self.ok_button = ok_button

        cancel_button = wx.Button(self, label=L('CANCEL'))
        self.cancel_button = cancel_button

        ok_button.Bind(wx.EVT_BUTTON, self.on_close)

        cancel_button.Bind(wx.EVT_BUTTON, self.on_close)

        hbox.Add(cancel_button)
        hbox.Add(ok_button, flag=wx.RIGHT, border=5)

        return hbox

    def get_line(self):
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        return line

    def set_legends_parent_values(self):
        # --- Para Cluster
        if self.GetParent().visualization_mode == 0:
            self.GetParent().legends_cluster = self.page_cluster.g_values()

        # -- Para Resumen
        if self.GetParent().visualization_mode == 1:
            self.GetParent().legends_summary = self.page_resumes.g_values()
            r1 = self.page_resumes.color_radio1
            self.GetParent().summ_dif_color = r1.GetValue()

        # --- Para Cluster y Resumen
        if self.GetParent().visualization_mode == 2:
            _clus, _sum = self.page_cluster_sumary.g_values()
            self.GetParent().legends_cluster = _clus
            self.GetParent().legends_summary = _sum
            r1 = self.page_cluster_sumary.color_radio1
            self.GetParent().data_summ_dif_color = r1.GetValue()

    def set_axes_parent_values(self):
        # ---- Para Cluster
        self.GetParent().clus_one_axe = self.clus_ax_rd1.GetValue()

#         Para Resumen
        self.GetParent().summ_one_axe = self.summ_ax_rd1.GetValue()

#         Para Ambos
        self.GetParent().clus_summ_axs = []
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd1.GetValue())
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd2.GetValue())
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd3.GetValue())
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd4.GetValue())

    def update_language(self, message):
        self.SetTitle(L('CLUSTER_CONFIG'))
        self.sbox_mv.SetLabel(L('DISPLAY_MODE'))
        self.nb.SetPageText(2, L('CLUSTERS_AND_SUMMARIES'))
        self.nb.SetPageText(1, L('SUMMARIES'))
        self.ok_button.SetLabel(L('OK'))
        self.cancel_button.SetLabel(L('CANCEL'))

    def on_close(self, e):
        self.set_axes_parent_values()
        self.set_legends_parent_values()
        self.Close()

    def pre_show(self):
        if self.GetParent().cb_shape.GetValue() and \
                self.GetParent().cb_kmeans.GetValue():
            self.page_cluster.radio1.SetValue(True)
            self.page_cluster.radio2.Disable()
            self.page_resumes.radio1.SetValue(True)
            self.page_resumes.radio2.Disable()
            self.page_cluster_sumary.radio1.SetValue(True)
            self.page_cluster_sumary.radio2.Disable()
            self.page_cluster_sumary.radio3.Disable()
            self.page_cluster_sumary.r4.Disable()
        else:
            self.page_cluster.radio2.Enable()
            self.page_resumes.radio2.Enable()
            self.page_cluster_sumary.radio2.Enable()
            self.page_cluster_sumary.radio3.Enable()
            self.page_cluster_sumary.r4.Enable()


class ClusterPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sboxs_ax = self.get_axes(dialog_ref)
        sboxs_lg = self.get_legends(dialog_ref)

        sizer.Add(sboxs_ax, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        self.SetSizer(sizer)

    def get_axes(self, dialog_ref):
        self.sbox_ax = wx.StaticBox(self, -1, L('DISPLAY_SELECTED'))
        sboxs_ax = wx.StaticBoxSizer(self.sbox_ax, wx.VERTICAL)

        _title = L('IN_A_FIGURE')
        self.radio1 = wx.RadioButton(self, -1, _title, style=wx.RB_GROUP)
        self.radio1.SetValue(False)
        dialog_ref.clus_ax_rd1 = self.radio1

        self.radio2 = wx.RadioButton(self, -1, L('IN_DIFFERENT_FIGURES'))
        dialog_ref.clus_ax_rd2 = self.radio2

        sboxs_ax.Add(self.radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(self.radio2, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        self.sbox_lg = wx.StaticBox(self, -1, L('LEGEND_CONTENT'))
        sboxs_lg = wx.StaticBoxSizer(self.sbox_lg, wx.VERTICAL)

        self.checkbox1 = wx.CheckBox(self, -1, L('PERCENTAGE_OF_OBSERVATIONS'))
        dialog_ref.clus_lg_check1 = self.checkbox1

        self.checkbox2 = wx.CheckBox(self, -1, L('AMOUNT_OF_OBSERVATIONS'))
        dialog_ref.clus_lg_check2 = self.checkbox2

        self.checkbox3 = wx.CheckBox(self, -1, L('NAME'))
        dialog_ref.clus_lg_check3 = self.checkbox3
        self.checkbox3.SetValue(True)

        self.checkbox4 = wx.CheckBox(self, -1, L('SHAPES'))
        dialog_ref.clus_lg_check4 = self.checkbox4

        sboxs_lg.Add(self.checkbox1, 0, wx.ALL, 5)
        sboxs_lg.Add(self.checkbox2, 0, wx.ALL, 5)
        sboxs_lg.Add(self.checkbox3, 0, wx.ALL, 5)
        sboxs_lg.Add(self.checkbox4, 0, wx.ALL, 5)

        return sboxs_lg

    def update_language(self, message):
        self.sbox_ax.SetLabel(L('DISPLAY_SELECTED'))
        self.radio1.SetLabel(L('IN_A_FIGURE'))
        self.radio2.SetLabel(L('IN_DIFFERENT_FIGURES'))

        self.sbox_lg.SetLabel(L('LEGEND_CONTENT'))
        self.checkbox1.SetLabel(L('PERCENTAGE_OF_OBSERVATIONS'))
        self.checkbox2.SetLabel(L('AMOUNT_OF_OBSERVATIONS'))
        self.checkbox3.SetLabel(L('NAME'))
        self.checkbox4.SetLabel(L('SHAPES'))

    def g_values(self):
        return [self.checkbox1.GetValue(), self.checkbox2.GetValue(),
                self.checkbox3.GetValue(), self.checkbox4.GetValue()]


class SummaryPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sboxs_ax = self.get_axes(dialog_ref)
        sboxs_lc = self.get_legends_colors(dialog_ref)
        sboxs_lg = self.get_legends(dialog_ref)

        sizer.Add(sboxs_ax, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lc, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        self.SetSizer(sizer)

    def get_axes(self, dialog_ref):

        self.sbox_ax = wx.StaticBox(self, -1, L('DISPLAY_SELECTED'))
        sboxs_lc = wx.StaticBoxSizer(self.sbox_ax, wx.VERTICAL)

        _title = L('IN_A_FIGURE')
        self.radio1 = wx.RadioButton(self, -1, _title, style=wx.RB_GROUP)
        self.radio1.SetValue(False)
        dialog_ref.summ_ax_rd1 = self.radio1

        self.radio2 = wx.RadioButton(self, -1, L('IN_DIFFERENT_FIGURES'))
        dialog_ref.summ_ax_rd2 = self.radio2

        sboxs_lc.Add(self.radio1, 0, wx.ALL, 5)
        sboxs_lc.Add(self.radio2, 0, wx.ALL, 5)

        return sboxs_lc

    def get_legends_colors(self, dialog_ref):
        self.sbox_lc = wx.StaticBox(self, -1, L('COLOR_SUMM'))
        sboxs_ax = wx.StaticBoxSizer(self.sbox_lc, wx.VERTICAL)

        _title = L('COLOR_SUMM_SUMM')
        self.color_radio1 = wx.RadioButton(self, -1, _title, style=wx.RB_GROUP)
        self.color_radio1.SetValue(True)

        self.color_radio2 = wx.RadioButton(self, -1, L('COLOR_SUMM_CLUS'))

        sboxs_ax.Add(self.color_radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(self.color_radio2, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        self.sbox_lg = wx.StaticBox(self, -1, L('LEGEND_CONTENT'))
        sboxs_lg = wx.StaticBoxSizer(self.sbox_lg, wx.VERTICAL)

        self.checkbox1 = wx.CheckBox(self, -1, L('PERCENTAGE_OF_OBSERVATIONS'))
        self.checkbox1.SetValue(True)
        dialog_ref.summ_lg_check1 = self.checkbox1

        self.checkbox2 = wx.CheckBox(self, -1, L('AMOUNT_OF_OBSERVATIONS'))
        dialog_ref.summ_lg_check2 = self.checkbox2

        self.checkbox3 = wx.CheckBox(self, -1, L('NAME'))
        dialog_ref.summ_lg_check3 = self.checkbox3

        self.checkbox4 = wx.CheckBox(self, -1, L('SHAPES'))
        dialog_ref.summ_lg_check4 = self.checkbox4

        sboxs_lg.Add(self.checkbox1, 0, wx.ALL, 5)
        sboxs_lg.Add(self.checkbox2, 0, wx.ALL, 5)
        sboxs_lg.Add(self.checkbox3, 0, wx.ALL, 5)
        sboxs_lg.Add(self.checkbox4, 0, wx.ALL, 5)

        return sboxs_lg

    def update_language(self, message):
        self.sbox_ax.SetLabel(L('DISPLAY_SELECTED'))
        self.radio1.SetLabel(L('IN_A_FIGURE'))
        self.radio2.SetLabel(L('IN_DIFFERENT_FIGURES'))

        self.sbox_lg.SetLabel(L('LEGEND_CONTENT'))
        self.checkbox1.SetLabel(L('PERCENTAGE_OF_OBSERVATIONS'))
        self.checkbox2.SetLabel(L('AMOUNT_OF_OBSERVATIONS'))
        self.checkbox3.SetLabel(L('NAME'))
        self.checkbox4.SetLabel(L('SHAPES'))

    def g_values(self):
        return [self.checkbox1.GetValue(), self.checkbox2.GetValue(),
                self.checkbox3.GetValue(), self.checkbox4.GetValue()]


class ClusterSummaryPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sboxs_ax = self.get_axes(dialog_ref)
        sboxs_lg = self.get_legends(dialog_ref)

        sizer.Add(sboxs_ax, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        self.SetSizer(sizer)

    def get_axes(self, dialog_ref):
        self.sbox_ax = wx.StaticBox(self, -1, L('DISPLAY_SELECTED'))
        sboxs_ax = wx.StaticBoxSizer(self.sbox_ax, wx.VERTICAL)

        _title = L('ALL_IN_SAME_FIGURE')
        self.radio1 = wx.RadioButton(self, -1, _title, style=wx.RB_GROUP)
        self.radio1.SetValue(False)
        dialog_ref.clus_summ_ax_rd1 = self.radio1

        self.radio2 = wx.RadioButton(self, -1, L('ALL_IN_DIFFERENT_FIGURES'))
        dialog_ref.clus_summ_ax_rd2 = self.radio2

        _title = L('A_FIGURE_FOR_EACH_CLUSTER_AND_SUMMARY')
        self.radio3 = wx.RadioButton(self, -1, _title)
        dialog_ref.clus_summ_ax_rd3 = self.radio3

        _title = L('CLUSTERS_IN_A_FIGURE_AND_SUMMARIES_IN_ANOTHER')
        self.r4 = wx.RadioButton(self, -1, _title)
        dialog_ref.clus_summ_ax_rd4 = self.r4

        sboxs_ax.Add(self.radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(self.radio2, 0, wx.ALL, 5)
        sboxs_ax.Add(self.radio3, 0, wx.ALL, 5)
        sboxs_ax.Add(self.r4, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        self.sbox_lg = wx.StaticBox(self, -1, L('LEGEND'))
        sboxs_lg = wx.StaticBoxSizer(self.sbox_lg, wx.VERTICAL)

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.get_cluster_legend(nb, dialog_ref), "Cluster")
        nb.AddPage(self.get_summary_legend(nb, dialog_ref), L('SUMMARY'))
        nb.AddPage(self.get_color_legend(nb, dialog_ref), L('COLOR_SUMM'))
        self.nb = nb

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        sboxs_lg.Add(p, 0, wx.ALL | wx.EXPAND, 5)
        return sboxs_lg

    def get_cluster_legend(self, parent, dialog_ref):

        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        _title = L('SHOW_PERCENTAGE_OF_OBSERVATIONS')
        self.checkbox1 = wx.CheckBox(panel, -1, _title)
        dialog_ref.clus_lg_check1 = self.checkbox1

        self.checkbox2 = wx.CheckBox(panel, -1,
                                     L('SHOW_AMOUNT_OF_OBSERVATIONS'))
        dialog_ref.clus_lg_check2 = self.checkbox2

        self.checkbox3 = wx.CheckBox(panel, -1, L('SHOW_NAME'))
        dialog_ref.clus_lg_check3 = self.checkbox3

        self.checkbox4 = wx.CheckBox(panel, -1, L('SHOW_SHAPES'))
        self.checkbox4.SetValue(True)
        dialog_ref.clus_lg_check4 = self.checkbox4

        sizer.Add(self.checkbox1, 0, wx.ALL, 5)
        sizer.Add(self.checkbox2, 0, wx.ALL, 5)
        sizer.Add(self.checkbox3, 0, wx.ALL, 5)
        sizer.Add(self.checkbox4, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel

    def get_summary_legend(self, parent, dialog_ref):

        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        checkbox1 = wx.CheckBox(panel, -1,
                                L('SHOW_PERCENTAGE_OF_OBSERVATIONS'))
        checkbox1.SetValue(True)
        dialog_ref.summ_lg_check1 = checkbox1
        self.chkbox1 = checkbox1

        checkbox2 = wx.CheckBox(panel, -1, L('SHOW_AMOUNT_OF_OBSERVATIONS'))
        dialog_ref.summ_lg_check2 = checkbox2
        self.chkbox2 = checkbox2

        checkbox3 = wx.CheckBox(panel, -1, L('SHOW_NAME'))
        dialog_ref.summ_lg_check3 = checkbox3
        self.chkbox3 = checkbox3

        checkbox4 = wx.CheckBox(panel, -1, L('SHOW_SHAPES'))
        dialog_ref.summ_lg_check4 = checkbox4
        self.chkbox4 = checkbox4

        sizer.Add(checkbox1, 0, wx.ALL, 5)
        sizer.Add(checkbox2, 0, wx.ALL, 5)
        sizer.Add(checkbox3, 0, wx.ALL, 5)
        sizer.Add(checkbox4, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel

    def get_color_legend(self, parent, dialog_ref):

        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        _titl = L('COLOR_SUMM_SUMM')
        self.color_radio1 = wx.RadioButton(panel, -1, _titl, style=wx.RB_GROUP)
        self.color_radio1.SetValue(True)

        self.color_radio2 = wx.RadioButton(panel, -1, L('COLOR_SUMM_CLUS'))

        sizer.Add(self.color_radio1, 0, wx.ALL, 5)
        sizer.Add(self.color_radio2, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel

    def update_language(self, message):
        self.sbox_ax.SetLabel(L('DISPLAY_SELECTED'))
        self.radio1.SetLabel(L('ALL_IN_SAME_FIGURE'))
        self.radio2.SetLabel(L('ALL_IN_DIFFERENT_FIGURES'))
        self.radio3.SetLabel(L('A_FIGURE_FOR_EACH_CLUSTER_AND_SUMMARY'))
        self.r4.SetLabel(L('CLUSTERS_IN_A_FIGURE_AND_SUMMARIES_IN_ANOTHER'))

        self.sbox_lg.SetLabel(L('DISPLAY_SELECTED'))
        self.nb.SetPageText(1, L('SUMMARY'))

        self.checkbox1.SetLabel(L('SHOW_PERCENTAGE_OF_OBSERVATIONS'))
        self.checkbox2.SetLabel(L('SHOW_AMOUNT_OF_OBSERVATIONS'))
        self.checkbox3.SetLabel(L('SHOW_NAME'))
        self.checkbox4.SetLabel(L('SHOW_SHAPES'))

        self.chkbox1.SetLabel(L('SHOW_PERCENTAGE_OF_OBSERVATIONS'))
        self.chkbox2.SetLabel(L('SHOW_AMOUNT_OF_OBSERVATIONS'))
        self.chkbox3.SetLabel(L('SHOW_NAME'))
        self.chkbox4.SetLabel(L('SHOW_SHAPES'))

    def g_values(self):
        _clus = [self.checkbox1.GetValue(), self.checkbox2.GetValue(),
                 self.checkbox3.GetValue(), self.checkbox4.GetValue()]

        _sum = [self.chkbox1.GetValue(), self.chkbox2.GetValue(),
                self.chkbox3.GetValue(), self.chkbox4.GetValue()]
        return _clus, _sum


class FilterClusterDialog(wx.Dialog):
    def __init__(self, parent, data):
        wx.Dialog.__init__(self, parent, title=L('CLUSTER_FILTER'),
                           size=(400, 390))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        self.parent = parent
        self.data = data

        sboxs_fc = self.set_filter_config()

        line = self.get_line()

        sbuttons = self.set_buttons()

        vsizer = wx.BoxSizer(wx.VERTICAL)

        vsizer.Add(sboxs_fc, 0, wx.EXPAND | wx.ALL, 7)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vsizer, 0, wx.EXPAND)
        _style = wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP
        sizer.Add(line, 0, _style, 5)
        sizer.Add(sbuttons, flag=wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM,
                  border=10)

        self.SetSizer(sizer)

        self.ShowModal()

    def _init_value(self, data):
        if data.option == 0:
            self.radio1.SetValue(True)
        elif data.option == 1:
            self.radio2.SetValue(True)
            self.first_repre.SetValue(data.more_repre)
        elif data.option == 2:
            self.radio3.SetValue(True)
            self.less_repre.SetValue(data.less_repre)
        elif data.option == 3:
            self.radio4.SetValue(True)
            self.lb1.SetChecked(data.max_objetives_use)
            self.lb2.SetChecked(data.min_objetives_use)

    def on_cancel(self, event):
        self.parent.data_selected.cancel = True
        self.Close()

    def on_accept(self, event):
        self.parent.data_selected.cancel = False
        self.Close()

    def get_line(self):
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        return line

    def set_buttons(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, label=L('OK'))
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_accept)

        self.cancel_button = wx.Button(self, label=L('CANCEL'))
        self.cancel_button.SetDefault()
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        hbox.Add(self.cancel_button)
        hbox.Add(self.ok_button, flag=wx.RIGHT, border=5)

        return hbox

    def update_button(self):
        page = self.parent.data_selected.option
        self.ok_button.Disable()

        if page == 0:
            _v = self.more_repre.GetValue() + self.less_repre.GetValue()
            if _v != 0:
                self.ok_button.Enable()
                self.ok_button.SetDefault()
        elif page == 1:
            _v = len(self.lb1.GetChecked()) + len(self.lb2.GetChecked())
            if _v != 0:
                self.ok_button.Enable()
                self.ok_button.SetDefault()

    def set_filter_config(self):
        self.sbox_fc = wx.StaticBox(self, -1, L('FILTER_CONFIG'))
        sboxs_fc = wx.StaticBoxSizer(self.sbox_fc, wx.HORIZONTAL)

        p = wx.Panel(self)
        nb = wx.Choicebook(p, -1)

        _label = L('REPRESENTATIVITY_IN_QUANTITY')
        nb.AddPage(self.get_more_representative(nb), _label)

        _label = L('REPRESENTATIVITY_VALUES_OBJECTIVES')
        nb.AddPage(self.get_representative_per_obj(nb), _label)

        nb.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_page_changed)

        self.nb = nb

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND | wx.EXPAND, 5)
        p.SetSizer(sizer)

        sboxs_fc.Add(p, 1, wx.ALL | wx.EXPAND, 5)
        return sboxs_fc

    def on_page_changed(self, e):
        selection = e.GetSelection()

        self.parent.data_selected.max_repre = self.more_repre.GetMax()

        if selection == 0:
            self.parent.data_selected.option = 0
            self.parent.data_selected.more_repre = self.more_repre.GetValue()
            self.parent.data_selected.less_repre = self.less_repre.GetValue()
            self.update_button()

        elif selection == 1:
            self.parent.data_selected.option = 1
            self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
            self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()
            self.update_button()

        e.Skip()

    def get_more_representative(self, parent):
        panel = wx.Panel(parent)

        self.sbox_sf = wx.StaticBox(panel, -1,
                                    L('MORE_REPRESENTATIVE_CLUSTER'))
        sboxs_sf = wx.StaticBoxSizer(self.sbox_sf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=2)
        lbl = wx.StaticText(panel, -1, L('SET_THE_AMOUNT'))
        self.more_repre = wx.SpinCtrl(panel, 0, "", (30, 50))
        self.more_repre.SetRange(0, self.data.count_tendency)
        self.more_repre.SetValue(self.data.more_repre)
        self.more_repre.Bind(wx.EVT_SPINCTRL, self.on_more_repre)
        grid.Add(lbl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid.Add(self.more_repre, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_sf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        self.sbox_sf1 = wx.StaticBox(panel, -1,
                                     L('LESS_REPRESENTATIVE_CLUSTER'))
        sboxs_sf1 = wx.StaticBoxSizer(self.sbox_sf1, wx.VERTICAL)
        grid1 = wx.FlexGridSizer(cols=2)
        lbl = wx.StaticText(panel, -1, L('SET_THE_AMOUNT'))
        self.less_repre = wx.SpinCtrl(panel, 0, "", (30, 50))
        self.less_repre.SetRange(0, self.data.count_tendency)
        self.less_repre.SetValue(self.data.more_repre)
        self.less_repre.Bind(wx.EVT_SPINCTRL, self.on_less_repre)

        self.lbl = lbl
        grid1.Add(lbl, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid1.Add(self.less_repre, 1, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_sf1.Add(grid1, 1, wx.EXPAND | wx.ALL, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sboxs_sf, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sboxs_sf1, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel

    def on_more_repre(self, event):
        self.parent.data_selected.more_repre = self.more_repre.GetValue()
        self.update_button()

    def on_less_repre(self, event):
        self.parent.data_selected.less_repre = self.less_repre.GetValue()
        self.update_button()

    def get_representative_per_obj(self, parent):
        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=3)

        sizer_lb1 = wx.BoxSizer(wx.VERTICAL)
        lb1_label = wx.StaticText(panel, -1, L('HIGHER_VALUES'))
        pts = lb1_label.GetFont().GetPointSize()
        lb1_label.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb1_label = lb1_label
        self.lb1 = wx.CheckListBox(panel, choices=self.data.max_objetives,
                                   size=(100, 160))
        self.lb1.Bind(wx.EVT_CHECKLISTBOX, self.on_lb1)

        sizer_lb1.Add(lb1_label, flag=wx.ALL, border=2)
        sizer_lb1.Add(self.lb1, flag=wx.ALL | wx.EXPAND, border=5)

        sizer_lb2 = wx.BoxSizer(wx.VERTICAL)
        lb2_label = wx.StaticText(panel, -1, L('SMALLER_VALUES'))
        pts = lb2_label.GetFont().GetPointSize()
        lb2_label.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb2_label = lb2_label
        self.lb2 = wx.CheckListBox(panel, choices=self.data.max_objetives,
                                   size=(100, 160))
        self.lb2.Bind(wx.EVT_CHECKLISTBOX, self.on_lb2)
        sizer_lb2.Add(lb2_label, flag=wx.ALL, border=2)
        sizer_lb2.Add(self.lb2, flag=wx.ALL | wx.EXPAND, border=5)

        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(sizer_lb1, 0, _style, 5)
        grid.Add(wx.StaticLine(panel, wx.ID_ANY, style=wx.LI_VERTICAL), 0,
                 wx.ALL | wx.EXPAND, 5)
        _style = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(sizer_lb2, 0, _style, 5)

        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        return panel

    def on_lb1(self, event):
        self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
        self.update_button()

    def on_lb2(self, event):
        self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()
        self.update_button()

    def update_language(self, message):
        self.SetTitle(L('CLUSTER_FILTER'))
        self.ok_button.SetLabel(L('OK'))
        self.cancel_button.SetLabel(L('CANCEL'))

        self.sbox_fc.SetLabel(L('FILTER_CONFIG'))
        self.nb.SetPageText(0, L('REPRESENTATIVITY_IN_QUANTITY'))
        self.nb.SetPageText(1, L('REPRESENTATIVITY_VALUES_OBJECTIVES'))

        self.sbox_sf.SetLabel(L('MORE_REPRESENTATIVE_CLUSTER'))
        self.lbl.SetLabel(L('SET_THE_AMOUNT'))
        self.sbox_sf1.SetLabel(L('LESS_REPRESENTATIVE_CLUSTER'))

        self.lb1_label.SetLabel(L('HIGHER_VALUES'))
        self.lb2_label.SetLabel(L('SMALLER_VALUES'))

    def update_by_generateClusters(self, max_value):
        self.more_repre.SetRange(0, max_value)
        self.more_repre.SetValue(0)
        self.less_repre.SetRange(0, max_value)
        self.less_repre.SetValue(0)


class SelectedData():
    def __init__(self):

        # ---- opción seleccionado
        self.option = None

        # ---- cantidad de tendencias existentes
        self.count_tendency = None

        # ---- más representivos
        self.more_repre = None

        # ---- menos representativos
        self.less_repre = None

        # ----  cancelar la selección
        self.cancel = True

        # ---- valores de objetivos mayores
        self.max_objetives = []
        self.max_objetives_use = []
        self.min_objetives_use = []


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        self.SetSize((300, 200))
        self.SetTitle('About dialog box')
        self.Centre()
        self.Show(True)
        self.SetPosition((0, 0))

        ClusterConfig(self)


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
