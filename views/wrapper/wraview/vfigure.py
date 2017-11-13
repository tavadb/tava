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
# Creado:  1/9/2016                                          ###
#                                                            ###
# ##############################################################
'''

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from mpldatacursor.datacursor import HighlightingDataCursor
import threading
from wx import GetTranslation as L
import wx
from wx.lib.itemspicker import ItemsPicker, EVT_IP_SELECTION_CHANGED

from wx.lib.pubsub import Publisher as pub

from imgs.ifigure import settings_fig, play_fig, sort_and_filter, \
    line_highligh
from languages import topic as T
from views.wrapper.vdialog.vfigured import FigureConfigDialog, AxesConfig, \
                                           FigureConfig, RadarChadConfig
from views.wrapper.wraview.vgraphic.figures import radarchart, kradviz, \
    kparallelcoordinates


K_PARALLEL_COORDENATE = 0
K_RADAR_CHART_POLYGON = 1
K_RADVIZ = 2
K_ANDREWS_CURVES = 3
K_RADAR_CHART_CIRCLE = 4
K_SCATTER_MATRIX = 5
K_SOM = 6
K_HITMAP = 7


class FigurePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#DCE5EE')

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        self.control_panel = None
        self.dframes = []
        self.order_names = []
        self.key_figure = 1
        self.mode_run = False

        self.current_dataframes = None
        self.current_datacolors = None

        self.run_explorer = False

        self.figure_config_dialog_ref = None

        # ---- inicialización de figura
        self.fig = Figure()
        self.canvas = FigureCanvas(self, -1, self.fig)

        # ---- configuración de figura
        self.fig_config = FigureConfig()
        self.set_figure_config()

        # ---- configuración de axe
        self.ax_conf = AxesConfig()

        # ---- radar chard config
        self.radar_chard_con = RadarChadConfig()

        # ---- toolbar
        self.sizer_tool = wx.BoxSizer(wx.HORIZONTAL)
        _bitmap = play_fig.GetBitmap()
        self.b_play = wx.BitmapButton(self, -1, _bitmap, style=wx.NO_BORDER)
        self.sizer_tool.Add(self.b_play, flag=wx.ALIGN_CENTER_VERTICAL)
        self.b_play.Bind(wx.EVT_BUTTON, self.on_play)
        self.b_play.SetToolTipString(L('VISUALIZE_DATE_CLUSTER'))
        _bitmap = settings_fig.GetBitmap()
        self.b_setting = wx.BitmapButton(self, -1, _bitmap, style=wx.NO_BORDER)
        self.sizer_tool.Add(self.b_setting, flag=wx.ALIGN_CENTER_VERTICAL)
        self.b_setting.Bind(wx.EVT_BUTTON, self.on_config)
        self.b_setting.SetToolTipString(L('FIGURE_CONF'))

        _bitmap = sort_and_filter.GetBitmap()
        self.b_sorted = wx.BitmapButton(self, -1, _bitmap, style=wx.NO_BORDER)
        self.b_sorted.Bind(wx.EVT_BUTTON, self.on_sort_and_filter)
        self.b_sorted.SetToolTipString(L('BUTTON_ORDER_AND_FILTER'))
        self.b_sorted.Disable()
        self.sizer_tool.Add(self.b_sorted, 0, wx.ALIGN_CENTER_VERTICAL)

        _bp = line_highligh.GetBitmap()
        self.b_highligh = wx.BitmapButton(self, -1, _bp, style=wx.NO_BORDER)
        self.b_highligh.Bind(wx.EVT_BUTTON, self.on_highligh)
        self.b_highligh.SetToolTipString(L('BUTTON_HIGHLIGHT'))
        self.b_highligh.Disable()
        self.sizer_tool.Add(self.b_highligh, 0, wx.ALIGN_CENTER_VERTICAL)

        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.toolbar.SetBackgroundColour('#DCE5EE')

        self.sizer_tool.Add(self.toolbar, 0, wx.ALIGN_CENTER_VERTICAL)

        choice_grafic = self.get_choice_grafic()
        self.sizer_tool.Add(choice_grafic, wx.ALIGN_LEFT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_tool, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Fit()
        self._welcome()

    def _welcome(self):
        Axes3D(self.fig)

    def set_figure_config(self):

        self.fig.set_figwidth(self.fig_config.width)
        self.fig.set_figheight(self.fig_config.height)
        self.fig.set_facecolor(self.fig_config.facecolor)

        left = self.fig_config.subplot_left
        bottom = self.fig_config.subplot_bottom
        right = self.fig_config.subplot_right
        top = self.fig_config.subplot_top
        wspace = self.fig_config.subplot_wspace
        hspace = self.fig_config.subplot_hspace
        self.fig.subplots_adjust(left, bottom, right, top, wspace, hspace)

        self.fig.suptitle('Tava Tool', fontsize=14, fontweight='light',
                          style='italic', family='serif', color='c',
                          horizontalalignment='center',
                          verticalalignment='center')

    def draw_graphic(self, dframes, colors):
        key_figure = self.g_figure()
        if key_figure == K_PARALLEL_COORDENATE:
            return kparallelcoordinates(dframes, 'Name', self.fig,
                                        self.ax_conf, self.fig_config,
                                        colors)

        elif key_figure == K_RADAR_CHART_POLYGON:
            return radarchart(dframes, 'Name', self.fig, self.ax_conf,
                              self.radar_chard_con, colors)
        elif key_figure == K_RADVIZ:
            return kradviz(dframes, 'Name', self.fig, self.ax_conf, colors)

    def kdraw(self, dframes, colors, ldic):

        self.current_dataframes = dframes
        self.current_datacolors = colors
        self.ldic = ldic
        self._kdraw(dframes, colors)

    def pre_kdraw_order(self, names_ordered):
        names_ordered.append('Name')
        _dframes = []
        for df in self.current_dataframes:
            _dframes.append(df[names_ordered])

        self._kdraw(_dframes, self.current_datacolors)

    def _kdraw(self, dframes, colors):
        self.fig.clear()
        self.start_busy()
        task = DrawThread(self, dframes, colors)
        task.start()

    def on_play(self, event):
        self.mode_run = True
        self.run_explorer = True
        self.new_order = []
        # ---- dibujar clusters/datos seleccionados
        self.control_panel.run_fig()

    def on_sort_and_filter(self, event):

        self.run_explorer = True
        cdf = self.current_dataframes
        if cdf is None or cdf == []:
            return

        self.old_order = cdf[0].columns.tolist()[:-1]
        ItemsPickerFilterDialog(self, self.old_order)

    def on_highligh(self, event):
        _label_aux = ''
        if self.run_explorer:
            for axe in self.fig.get_axes():
                lines = []
                for line in axe.get_children():
                    if isinstance(line, Line2D):
                        if self.ldic.get(line.get_color()) is not None:
                            _label_aux = self.ldic.get(line.get_color())
                            line.set_label('shape = ' + self.ldic.get(line.get_color()))
                            lines.append(line)
                        else:
                            line.set_label('')
                h = resaltar(lines, highlight_color=self.ax_conf.highlight_color,
                             formatter='{label}'.format)
                if lines != []:
                    h.show_highlight(lines[0])
            self.run_explorer = False
            self.canvas_draw()

    def on_config(self, event):
        if self.figure_config_dialog_ref is None:
            self.figure_config_dialog_ref = FigureConfigDialog(self)
        else:
            self.figure_config_dialog_ref.nb.SetSelection(0)
            self.figure_config_dialog_ref.ShowModal()

    def g_figure(self):
        return self.ch_graph.GetSelection()

    def get_choice_grafic(self):
        grid = wx.FlexGridSizer(cols=2)
        sampleList = self.get_item_list()

        self.ch_graph = wx.Choice(self, -1, choices=sampleList)
        self.ch_graph.SetSelection(0)
        self.ch_graph.Bind(wx.EVT_CHOICE, self.on_graphic)
        self.ch_graph.SetToolTipString(L('SELECT_A_GRAPHIC'))

        grid.Add(self.ch_graph, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        return grid

    def get_item_list(self):
        return [L('PARALLEL_COORDINATES'), 'Radar Chart']

    def on_graphic(self, event):

        if event.GetString() != L('PARALLEL_COORDINATES') or not self.mode_run:
            self.b_highligh.Disable()
            return
        self.b_highligh.Enable()

    def update_language(self, msg):
        s = self.ch_graph.GetSelection()
        self.ch_graph.SetItems(self.get_item_list())
        self.ch_graph.SetSelection(s)
        self.ch_graph.SetToolTipString(L('SELECT_A_GRAPHIC'))
        self.b_setting.SetToolTipString(L('FIGURE_CONF'))
        self.b_play.SetToolTipString(L('VISUALIZE_DATE_CLUSTER'))

    def start_busy(self):
        pub().sendMessage(T.START_BUSY)
        self.b_play.Disable()
        self.toolbar.Disable()
        self.b_setting.Disable()
        self.ch_graph.Disable()
        self.b_highligh.Disable()
        self.b_sorted.Disable()

    def stop_busy(self):
        pub().sendMessage(T.STOP_BUSY)
        self.b_play.Enable()
        self.toolbar.Enable()
        self.b_setting.Enable()
        self.ch_graph.Enable()
        self.b_highligh.Enable()
        self.b_sorted.Enable()

    def canvas_draw(self):
        self.canvas.draw()

    def set_fig(self, fig):
        self.fig = fig


class DrawThread(threading.Thread):
    def __init__(self, panel, dframes, colors):
        super(DrawThread, self).__init__()
        # Attributes
        self.panel = panel
        self.dframes = dframes
        self.colors = colors

    def run(self):
        fig = self.panel.draw_graphic(self.dframes, self.colors)
        wx.CallAfter(self.panel.stop_busy)
        wx.CallAfter(self.panel.set_fig, fig)
        wx.CallAfter(self.panel.canvas_draw)


class ItemsPickerFilterDialog(wx.Dialog):
    def __init__(self, parent, names):
        wx.Dialog.__init__(self, parent, -1, L('BUTTON_ORDER_AND_FILTER'))
        self.parent = parent
        self.names = names

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.ip = ItemsPicker(self, -1, names,
                              L('PICKER_EXISTING'),
                              L('PICKER_FILTERED'), ipStyle=0)
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.on_selection_change)
        self.ip._source.SetMinSize((-1, 150))
        sizer.Add(self.ip, 1, wx.ALL, 10)

        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        cancel = wx.Button(self, label=L('NEW_PROJECT_CANCEL'))
        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.create = wx.Button(self, label=L('NOW_SHOW'))
        self.create.Bind(wx.EVT_BUTTON, self.on_ok)
        self.create.Disable()

        sizer_button.Add(cancel)
        sizer_button.Add(self.create)

        sizer.Add(sizer_button, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        self.itemCount = 3
        self.Fit()
        self.ShowModal()

    def on_selection_change(self, e):

        if len(e.GetItems()) < 2:
            self.create.Disable()
            return
        self.item_ordered = e.GetItems()
        self.create.Enable()

    def on_ok(self, e):
        self.parent.pre_kdraw_order(self.item_ordered)
        self.Close()

    def on_cancel(self, e):
        self.Close()


import matplotlib
from matplotlib.contour import ContourSet
from matplotlib.image import AxesImage
from matplotlib.collections import PathCollection, LineCollection
from matplotlib.collections import PatchCollection, PolyCollection, QuadMesh
from matplotlib.container import Container
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
from matplotlib.backend_bases import PickEvent



class resaltar(HighlightingDataCursor):
    def __init__(self, *args, **kwargs):
        HighlightingDataCursor.__init__(self, *args, **kwargs)


    def update(self, event, annotation):
        """Update the specified annotation."""
 
        for artist in self.highlights.values():
            if self.display == 'multiple':
                continue
            if self.display == 'one-per-axes':
                if event.mouseevent.inaxes is not artist.axes:
                    continue
            artist.set_visible(False)
        self.show_highlight(event.artist)
         
         
         
        # Get artist-specific information about the pick event
        info = self.event_info(event)
 
        if self.props_override is not None:
            info = self.props_override(**info)
 
        # Update the xy position and text using the formatter function
        annotation.set_text(self.formatter(**info))
        annotation.xy = info['x'], info['y']
 
        # Unfortnately, 3D artists are a bit more complex...
        # Also, 3D artists don't share inheritance. Use naming instead.
        if '3D' in type(event.artist).__name__:
            annotation.xy = event.mouseevent.xdata, event.mouseevent.ydata
 
        # In case it's been hidden earlier...
        annotation.set_visible(True)
 
        if self.keep_inside:
            self._keep_annotation_inside(annotation)
 
        event.canvas.draw()