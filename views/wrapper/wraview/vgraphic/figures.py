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
# Creado:  1/11/2016                                    ###
#                                                            ###
# ##############################################################
'''
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from pandas.compat import lrange
from pandas.core import common as com
from pandas.tools.plotting import radviz

import numpy as np
from views.wrapper.wraview.vgraphic.figuresutils import square_plot, g_colors
from matplotlib import rcParams


# #######################################################################
#        parallel coordinates
# #######################################################################
def kparallelcoordinates(dframes, class_column, fig, ax_conf, fg_conf, colors):

    s_row, s_col = square_plot(len(dframes), False)

    for i, df in enumerate(dframes):
        ax = fig.add_subplot(s_row, s_col, i + 1)
        _parallelcoordinates(df, ax, ax_conf, class_column, colors[i])
    return fig


# #######################################################################
#        Radar Chart (circle - polygon)
# #######################################################################
def radarchart(dframes, class_column, fig, ax_conf, rc_config, colors):
    rcParams.update({'font.size': 19})

    s_row, s_col = square_plot(len(dframes), False)
    for i, df in enumerate(dframes):
        if ax_conf.xticklabels is None:
            spoke_labels = df.columns[:-1]
        else:
            spoke_labels = ax_conf.xticklabels
            
        # ---- configuración de axe para radar chart
        
        theta = radar_factory(len(spoke_labels), rc_config.type)
        ax = fig.add_subplot(s_row, s_col, i + 1, projection='radar')

        # ----- configuración de ytick
        if not ax_conf.y_axis_show:
            ax.set_yticklabels([])
        
        ax.set_varlabels(spoke_labels)

        ax = _radarchart(df, ax, fig, ax_conf, class_column, rc_config, theta,
                    colors[i])
    return fig


# #######################################################################
#        RadViz
# #######################################################################
def kradviz(dframes, class_column, fig, ax_conf, colors):

    s_row, s_col = square_plot(len(dframes))
    for i, df in enumerate(dframes):
        ax = fig.add_subplot(s_row, s_col, i + 1)
        _radviz(df, ax, ax_conf, class_column, colors[i])

    return fig


# ----        Implementation Details ------------------------------------------


# #######################################################################
#        Detail - Parallel Coordinates
# #######################################################################

def _parallelcoordinates(frame, ax, ax_conf, class_column, color_values=None):
    """Parallel coordinates plotting.
    """

    # ---- varaibles globales
    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]

    # ---- usar columnas personalizada o predeterminada
    if ax_conf.cols is None:
        df = frame.drop(class_column, axis=1)
    else:
        df = frame[ax_conf.cols]

    # ---- cantidad de columnas de datos
    ncols = len(df.columns)

    # ---- determina valor para  xticks
    if ax_conf.xticks is not None:
        if not np.all(np.isreal(ax_conf.xticks)):
            raise ValueError('xticks specified must be numeric')
        elif len(ax_conf.xticks) != ncols:
            raise ValueError('Length of xticks must ' +
                             'match number of columns')
        x = ax_conf.xticks
    else:
        x = lrange(ncols)

    # ---- selección de colores - automático/personalizado
    if color_values is None:
        color_values = g_colors(len(classes), ax_conf.color)

    colors = dict(zip(classes, color_values))

    # ---- creación de leyenda por valor
    used_legends = set([])

    for i in range(n):
        y = df.iloc[i].values
        kls = class_col.iat[i]
        label = com.pprint_thing(kls)
        if label not in used_legends:
            used_legends.add(label)
            ax.plot(x, y, color=colors[kls], label=label)
        else:
            ax.plot(x, y, color=colors[kls])

    # ancho de ejes paralelos
    _lwidth = None
    if ax_conf.axvlines:
        for i in x:
            _lwidth = ax_conf.axv_line_width
            if i == 0 or i == x[-1]:
                _lwidth = ax_conf.axv_line_width * 2
            ax.axvline(i, linewidth=ax_conf.axv_line_width,
                       color=ax_conf.axv_line_color)

    # ---- configuración de tick - visualización, labels, colors
    ax.set_xticks(x)
    if ax_conf.xticklabels is not None:
        ax.set_xticklabels(ax_conf.xticklabels)
        ax.tick_params(axis='x', labelsize=ax_conf.xticklabelssize)
    else:
        x_t_labels = df.columns
        if ax_conf.x_label_latex_show:
            x_t_labels = ['$'+lx+'$' for lx in x_t_labels]
        ax.set_xticklabels(x_t_labels)
        ax.tick_params(axis='x', labelsize=ax_conf.xticklabelssize)

    ax.set_xlim(x[0], x[-1])
    ax.get_xaxis().set_visible(ax_conf.x_axis_show)
    ax.get_yaxis().set_visible(ax_conf.y_axis_show)
    ax.tick_params(axis='x', colors=ax_conf.x_axis_color)
    ax.tick_params(axis='y', colors=ax_conf.y_axis_color)

    ax.set_xlabel(ax_conf.x_axis_label, labelpad=-1)
    ax.xaxis.label.set_color(ax_conf.x_color_label)

    ax.set_ylabel(ax_conf.y_axis_label, labelpad=-1)
    ax.yaxis.label.set_color(ax_conf.y_color_label)

    # ---- configuración de spines
    ax.spines['top'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['top'].set_linewidth(0.1)
    ax.spines['bottom'].set_linewidth(0.1)
    ax.spines['left'].set_linewidth(0.1)
    ax.spines['right'].set_linewidth(0.1)
    
    ax.spines['top'].set_color(ax_conf.color_top_spine)
    ax.spines['bottom'].set_color(ax_conf.color_bottom_spine)
    ax.spines['left'].set_color(ax_conf.color_left_spine)
    ax.spines['right'].set_color(ax_conf.color_right_spine)

    # ---- configuración de leyenda
    if ax_conf.legend_show:
        _c = ax_conf.legend_edge_color
        ax.legend(prop={'size': ax_conf.legend_size},
                  loc=ax_conf.legend_loc,
                  fancybox=True).get_frame().set_edgecolor(_c)

    # ---- configuración de grid
    if ax_conf.grid_lines:
        ax.grid(color=ax_conf.grid_color, linestyle=ax_conf.grid_lines_style,
                linewidth=ax_conf.grid_linewidth,
                alpha=ax_conf.grid_color_alpha)

    return ax


# #######################################################################
#        Detail - Radar Chart
# #######################################################################
def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
    return verts


def radar_factory(num_vars, frame):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi / 2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def _radarchart(frame, ax, fig, ax_conf, class_column, rc_config,
                theta, color_values=None, alpha=0.05):

    # ---- varaibles globales
    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]
    df = frame.drop(class_column, axis=1)

    # ---- selección de colores - automático/personalizado
    if color_values is None:
        color_values = g_colors(len(classes), ax_conf.color)
    colors = dict(zip(classes, color_values))

    # ---- configuración de relleno
    if rc_config.fill:
        for ii in range(n):
            d = df.iloc[ii].values
            kls = class_col.iat[ii]
            ax.plot(theta, d, color=colors[kls])
            ax.fill(theta, d, facecolor=colors[kls], alpha=alpha)
    else:
        for ii in range(n):
            d = df.iloc[ii].values
            kls = class_col.iat[ii]
            ax.plot(theta, d, color=colors[kls])

    # ---- configuración de leyenda
    if ax_conf.legend_show:
        r_patch = []
        classes = []
        _c = ax_conf.legend_edge_color

        for k in colors.keys():
            r_patch.append(mpatches.Patch(color=colors[k], linewidth=0.1))
            classes.append(k)

        leg = fig.legend(r_patch, classes, ax_conf.legend_loc, fancybox=True,
                         prop={'size': ax_conf.legend_size})
        leg.get_frame().set_edgecolor(ax_conf.legend_edge_color)

    # ---- configuración de grid
    if ax_conf.grid_lines:
        ax.grid(True)
        ax.grid(color=ax_conf.grid_color,
                linestyle=ax_conf.grid_lines_style,
                linewidth=ax_conf.grid_linewidth,
                alpha=ax_conf.grid_color_alpha)
    else:
        ax.grid(False)

    return ax


# #######################################################################
#        Detail - RadViz
# #######################################################################
def _radviz(frame, ax, ax_conf, class_column, color_values=None):

    radviz(frame, class_column, ax=ax, color=color_values)

    # ---- configuración de leyenda
    if ax_conf.legend_show:
        _c = ax_conf.legend_edge_color
        ax.legend(prop={'size': ax_conf.legend_size},
                  loc=ax_conf.legend_loc,
                  fancybox=True).get_frame().set_edgecolor(_c)

    # ---- configuración de tick - visualización, labels, colors

    ax.get_xaxis().set_visible(ax_conf.x_axis_show)
    ax.get_yaxis().set_visible(ax_conf.y_axis_show)
    ax.tick_params(axis='x', colors=ax_conf.x_axis_color)
    ax.tick_params(axis='y', colors=ax_conf.y_axis_color)

    ax.set_xlabel(ax_conf.x_axis_label, labelpad=-1)
    ax.xaxis.label.set_color(ax_conf.x_color_label)

    ax.set_ylabel(ax_conf.y_axis_label, labelpad=-1)
    ax.yaxis.label.set_color(ax_conf.y_color_label)

    # configuración de spines
    ax.spines['top'].set_color(ax_conf.color_top_spine)
    ax.spines['bottom'].set_color(ax_conf.color_bottom_spine)
    ax.spines['left'].set_color(ax_conf.color_left_spine)
    ax.spines['right'].set_color(ax_conf.color_right_spine)
