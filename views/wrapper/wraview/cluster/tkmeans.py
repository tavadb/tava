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
# Creado:  23/10/2016                                        ###
#                                                            ###
# ##############################################################
'''

import operator
from scipy.cluster.vq import kmeans, vq
from pandas.tools.plotting import _get_standard_colors
from matplotlib import colors

import numpy as np
import pandas as pd
from views.wrapper.wraview.cluster.shape import Cluster


class Kmeans():

    population = 0
    clusters = []
    clusters_count = 0
    tendencies = []
    tendency_count = 0
    column_name = 'Name'
    cluster_checkeds = []
    cluster_uncheckeds = []
    name_objectives = []

    def __init__(self, df_population, clus=0, is_nor=True):
        self.population = len(df_population.values.tolist())
        df_population = self.normalize_date(df_population, is_nor)
        self.clusters = self.generate_clusters(df_population, clus)
        self.clusters_count = len(self.clusters)
        self.name_objectives = df_population.columns.tolist()[:-1]
        # self.full_normalization()
        self.set_color_clusters()

    def full_normalization(self):
        cs = []
        for c in self.clusters:
            cs.append(c.df_value)

        # ---- normalizar completo
        df = pd.concat(cs)
        df = self._nor(df)
        df_group = df.groupby(self.column_name)

        for c in self.clusters:
            c.full_nor = df_group.get_group(c.shape)
            c.df_resume_nor = c.g_resume(c.full_nor, c.shape)

    def set_color_clusters(self):

        _count = len(self.clusters)
        _colors = self.g_colors(_count*2)
        _clus_cols = _colors[:_count]
        _resu_cols = _colors[_count:]

        for i, c in enumerate(self.clusters):
            c.clus_color = [_clus_cols[i]]
            c.resu_color = [_resu_cols[i]]

    def g_colors(self, count):
        color_values = []
        for rgb in _get_standard_colors(count, None, 'random'):
            color_values.append(colors.rgb2hex(rgb))
        return color_values

    def _norFictureScaling(self, df):

        class_column = df.columns[-1]
        class_col = df[class_column]
        df = df.drop(class_column, axis=1)

        for name_col in df.columns:
            x = df[name_col]
            mi = min(x)
            ma = max(x)
            df[name_col] = [(j-mi)/(ma - mi) for j in x]

        df[class_column] = class_col
        return df

    def _norFrobenius(self, df):
        def normalize(series):
            a = min(series)
            b = max(series)
            return (series - a) / (b - a)
        class_column = df.columns[-1]
        class_col = df[class_column]
        df = df.drop(class_column, axis=1).apply(normalize)
        df[class_column] = class_col
        return df

    def normalize_date(self, df_population, is_nor):
        if is_nor:
            return self._norFictureScaling(df_population)

        return df_population

    def generate_clusters(self, df_population,  clus):
        df = df_population.drop(self.column_name, axis=1)
        # ---- forma de normalizar
        # whitened = whiten(df.values)

        whitened = df.values
        centroids, _ = kmeans(whitened, clus)
        indexes, _ = vq(whitened, centroids)

        # ---- resumenes o centroides
        resumes = {}
        for i, rs in enumerate(centroids):
            resumes[str(i)+'-k'] = np.concatenate((rs, [i]))

        # ---- se crea un dataframe de toda la población
        df_clusters = pd.DataFrame(whitened, columns=df.columns)
        indexes = [str(i)+'-k' for i in indexes]
        df_clusters['Name'] = indexes

        # ---- se crean grupos
        return self.generalized_shape(df_clusters, resumes)

    def generalized_shape(self, df_shapes, resumes):

        current_clusters = []

        # ---- optener las tendencias
        all_shapes = df_shapes[self.column_name].tolist()

        # ---- ordenarlos de mayor a menor
        _clusters, _clusters_counts = np.unique(all_shapes, return_counts=True)
        s_dt = dict(zip(_clusters, _clusters_counts))
        _clusters_frequency = sorted(s_dt.items(), key=operator.itemgetter(1))
        _clusters_frequency.reverse()

        # ---- agregar a lista de clusters
        df_group = df_shapes.groupby(self.column_name)
        i_name = 1
        for shape, freq in _clusters_frequency:
            _df = df_group.get_group(shape)
            _c = Cluster(str(i_name)+'-k', shape, freq, _df, self.population,
                         resumes[shape])
            current_clusters.append(_c)
            i_name += 1

        return current_clusters

    def g_checkeds(self):
        return [self.clusters[cl] for cl in self.cluster_checkeds]

    # ------------------ METODOS PARA ANALISIS SHAPES -----------
    # -----------------------------------------------------------

    def g_clusters_max_min_in_var(self, indexes_max, indexes_min):
        _indexes = []
        for i in indexes_max:
            _indexes = _indexes + self.g_clusters_max_in_var(i)
        for i in indexes_min:
            _indexes = _indexes + self.g_clusters_min_in_var(i)
        return _indexes

    def g_clusters_max_in_var(self, index):
        index_max = []
        max_values = [c.g_max_in_var(index) for c in self.clusters]
        _max = max(max_values)
        for i, m in enumerate(max_values):
            if m == _max:
                index_max.append(i)
#         _clusters = [self.clusters[i] for i in index_max]
#         return _clusters
        return index_max

    def g_clusters_min_in_var(self, index):
        index_min = []
        min_values = [c.g_min_in_var(index) for c in self.clusters]
        _min = min(min_values)
        for i, m in enumerate(min_values):
            if m == _min:
                index_min.append(i)
#         _clusters = [self.clusters[i] for i in index_min]
#         return _clusters
        return index_min

    def g_data_by_dr(self, s_clusters, legends_cluster,
                     legends_summary, d_col, crude=True):

        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _resumes = []
        _legends = []
        _clus_color = []
        _resu_color = []

        for c in s_clusters:
            # data
            _df = c.df_value.copy()
            # df = c.df_value.copy() if crude else c.full_nor.copy()
            _leg = c.g_legend(_legends, legends_cluster)
            _legends.append(_leg)
            _df[self.column_name] = [_leg] * c.count
            _clusters.append(_df)
            _clus_color.append(c.clus_color)

            # resume
            _dfr = c.df_resume.copy()
            # _dfr = c.df_resume.copy() if crude else c.df_resume_nor.copy()
            _leg = c.g_legend(_legends, legends_summary)
            _legends.append(_leg)
            _dfr[self.column_name] = [_leg]
            _resumes.append(_dfr)
            _resu_color.append(c.resu_color if d_col else c.clus_color)

        return _clusters, _clus_color, _resumes, _resu_color

    def g_legend(self, legends, legends_condition, repeat=False):
        _legend = ""

        if legends_condition[0]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.g_percent_format()

        if legends_condition[1]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + str(self.count)

        if legends_condition[2]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.name

        if legends_condition[3]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.shape

        if not repeat:
            while _legend in legends:
                _legend = _legend + "."
        return _legend

    def g_data_for_fig(self, s_clusters, legends_cluster, crude=True):

        # ---- si no contiene clusters
        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _legends = []
        _colors = []

        # ---- clsuters seleccionados y creción de legendas
        for c in s_clusters:
            _df = c.df_value.copy()
            # df = c.df_value.copy() if crude else c.full_nor.copy()
            _leg = c.g_legend(_legends, legends_cluster)
            _legends.append(_leg)
            _df[self.column_name] = [_leg] * c.count
            _clusters.append(_df)
            _colors.append(c.clus_color)

        return _clusters, _colors

    def g_resume_for_fig(self, s_clusters, legends_summary, d_col, crude=True):
        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _legends = []
        _colors = []
        for c in s_clusters:
            _df = c.df_resume.copy()
            # _df = c.df_resume.copy() if crude else c.df_resume_nor.copy()
            _leg = c.g_legend(_legends, legends_summary)
            _legends.append(_leg)
            _df[self.column_name] = [_leg]
            _clusters.append(_df)
            _colors.append(c.resu_color if d_col else c.clus_color)

        return _clusters, _colors
