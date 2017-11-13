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

from matplotlib import colors
import operator
from pandas.core.frame import DataFrame
from pandas.tools.plotting import _get_standard_colors

import numpy as np
import pandas as pd
import random as rm
import scipy.stats as st


class Shape():

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

        # ---- calculo de shape para cada elemento
        new_columns = df_population.columns.tolist()
        df_shapes = pd.DataFrame(columns=new_columns)
        for i, value in enumerate(df_population.values.tolist()):
            _shape = '_'.join([str(v+1) for v in np.argsort(value[:-1])])
            value[-1] = _shape
            df_shapes.loc[i] = value

        # ---- se obtienen las tendencias del conjunto de datos
        _t = df_shapes[self.column_name].drop_duplicates().tolist()
        self.tendencies = _t
        self.tendency_count = len(self.tendencies)

        # ---- misma cantidad de tendencias que clusters(análisis shapes)
        if clus < 1 or clus == self.tendency_count:
            return self.generalized_shape(df_shapes)

        # ---- cantidad de cluster menor a tendencias
        if clus < self.tendency_count:

            # selección aleatoria de shape
            i_distinct = range(len(self.tendencies))
            rm.shuffle(i_distinct)
            s_selected = [self.tendencies[s] for s in i_distinct[:clus]]
            r_selected = [self.tendencies[s] for s in i_distinct[clus:]]

            # caso especial
            if clus == 1:
                reemplaze = s_selected * self.population
                df_shapes[self.column_name] = reemplaze
                return self.generalized_shape(df_shapes)

            # unificamos los clusters mas cercanos
            for i, r_shape in enumerate(r_selected):
                l_rho = 2
                a_shape = ''

                for s_shape in s_selected:
                    _s = [int(_i) for _i in s_shape.split('_')]
                    _r = [int(_i) for _i in r_shape.split('_')]
                    rho, _pva = st.spearmanr(_s, _r)
                    if abs(rho) <= l_rho:
                        l_rho = abs(rho)
                        a_shape = s_shape
                df_shapes[self.column_name].replace(r_shape, a_shape,
                                                    inplace=True)

            return self.generalized_shape(df_shapes)

        # ---- número de clusters mayor a tendencias

        # ---- cantidad faltante de shape
        missing = clus - self.tendency_count

        # ---- cantidad de individuos por shape
        idividuos_x_shape = []
        tends = df_shapes[self.column_name].tolist()
        for t in self.tendencies:
            idividuos_x_shape.append(tends.count(t))

        # ---- cantidad inicial de clusters - todos a uno
        n_clusters_final = [1]*len(idividuos_x_shape)

        # --- eliminación de indices con cantidad de indivisuo menores a dos
        a_paricipar = []
        for i, v in enumerate(idividuos_x_shape):
            if v > 1:
                a_paricipar.append(i)

        # ---- calculo de número de clusters finales
        while missing != 0:
            _index = np.random.randint(len(a_paricipar))
            a = a_paricipar[_index]
            n_clusters_final[a] = n_clusters_final[a] + 1
            if idividuos_x_shape[a] == n_clusters_final[a]:
                del a_paricipar[_index]
            missing -= 1

        # ---- division se shape para clusters
        df_group = df_shapes.groupby(self.column_name)
        final_dfs = []
        for i, tend in enumerate(self.tendencies):
            df = df_group.get_group(tend).copy()
            n_clus = n_clusters_final[i]

            if n_clus > 1:

                c_indi = idividuos_x_shape[i]
                _mod = c_indi % n_clus
                ras = range(0, c_indi-_mod, c_indi/n_clus)
                ras.append(c_indi)
                _cols = df[self.column_name].tolist()

                sl = []
                _tend = df[self.column_name].tolist()

                for j in range(len(ras)-1):
                    _c = _tend[ras[j]:ras[j+1]]
                    sl = sl + [v+'-'+str(j) for v in _c]

                df[self.column_name] = sl
                final_dfs.append(df)

            else:
                final_dfs.append(df)

        return self.generalized_shape(pd.concat(final_dfs))

    def generalized_shape(self, df_shapes):

        current_clusters = []
        # optener las tendencias
        all_shapes = df_shapes[self.column_name].tolist()
        # ordenarlos de mayor a menor
        _clusters, _clusters_counts = np.unique(all_shapes, return_counts=True)
        s_dt = dict(zip(_clusters, _clusters_counts))
        _clusters_frequency = sorted(s_dt.items(), key=operator.itemgetter(1))
        _clusters_frequency.reverse()

        # agregar a lista de clusters
        df_group = df_shapes.groupby(self.column_name)
        i_name = 1
        for shape, freq in _clusters_frequency:
            _df = df_group.get_group(shape)
            _c = Cluster('G' + str(i_name), shape, freq, _df, self.population)
            current_clusters.append(_c)
            i_name += 1
        return current_clusters

    def frobenius_nor(self, df):
        df1 = df.drop(self.column_name, axis=1)
        nor = (lambda x: x / np.linalg.norm(x))
        dframe_nor = DataFrame(nor(df1.values.tolist()),
                               columns=df1.columns.tolist())
        dframe_nor[self.column_name] = df[self.column_name].tolist()
        return dframe_nor

    def rangecero_nor(self, df):
        for cols in df.columns[:-1]:
            vals = df[cols]
            _min = vals.min()
            _max = vals.max()
            _vnor = [(x - _min) / (_max - _min) for x in vals]
            df[cols] = _vnor
        return df

    def g_checkeds(self):
        return [self.clusters[cl] for cl in self.cluster_checkeds]

    def g_uncheckeds(self):
        return [self.clusters[cl] for cl in self.cluster_uncheckeds]

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

    def g_with_percent(self, percent):
        _clusters = []
        for c in self.clusters:
            if percent == c.g_percent():
                _clusters.append(c)
        return _clusters

    def g_percent_up(self, percent):
        _per = 0.0
        _clusters = []
        for c in self.clusters:
            _per = _per + c.g_percent(self.population)
            _clusters.append(c)
            if percent <= _per:
                return _clusters
        return _clusters

    def g_percent_up_resumes(self, percent):
        _per = 0.0
        df_resumes = pd.DataFrame()
        for c in self.clusters:
            serie_mean = c.df_value[c.df_value.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            df_mean[self.column_name] = c.shape
            df_resumes = df_resumes.append(df_mean)
            _per = _per + c.g_percent(self.population)
            if percent <= _per:
                return df_resumes
        return df_resumes

    def g_data_for_fig(self, s_clusters, legends_cluster, crude=True):

        # ---- si no contiene clusters
        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _legends = []
        _colors = []

        # ---- clsuters seleccionados y creción de legendas
        for c in s_clusters:
            # _df = c.df_value.copy() if crude else c.full_nor.copy()
            _df = c.df_value.copy()
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

    def g_data_and_resume_one_for_fig(self, s_clusters, legends_cluster,
                                      legends_summary, clus_summ_axs,
                                      crude=True):
        if s_clusters == []:
            return pd.DataFrame()
        _clusters = []
        _legends = []

        if clus_summ_axs[2]:
            for c in s_clusters:
                # data
                _df_c = c.df_value.copy() if crude else c.full_nor.copy()
                _df_c = c.df_value.copy() if crude else c.full_nor.copy()
                _leg = c.g_legend(_legends, legends_cluster)
                _legends.append(_leg)
                _df_c[self.column_name] = [_leg] * c.count

                # resume
                _df_s = c.df_resume.copy() if crude else c.df_resume_nor.copy()
                _leg = c.g_legend(_legends, legends_summary)
                _legends.append(_leg)
                _df_s[self.column_name] = [_leg]

                _clusters.append(pd.concat([_df_c, _df_s]))

            return _clusters

        if clus_summ_axs[3]:
            _datas = []
            _resumes = []
            for c in s_clusters:
                # data
                _df_c = c.df_value.copy() if crude else c.full_nor.copy()
                _leg = c.g_legend(_legends, legends_cluster)
                _legends.append(_leg)
                _df_c[self.column_name] = [_leg] * c.count
                _datas.append(_df_c)

                # resume
                _df_s = c.df_resume.copy() if crude else c.df_resume_nor.copy()
                _leg = c.g_legend(_legends, legends_summary)
                _legends.append(_leg)
                _df_s[self.column_name] = [_leg]
                _resumes.append(_df_s)

            _clusters.append(pd.concat(_datas))
            _clusters.append(pd.concat(_resumes))

            return _clusters

        for c in s_clusters:
            # data
            _df = c.df_value.copy() if crude else c.full_nor.copy()
            _leg = c.g_legend(_legends, legends_cluster)
            _legends.append(_leg)
            _df[self.column_name] = [_leg] * c.count
            _clusters.append(_df)
            # resume
            _df = c.df_resume.copy() if crude else c.df_resume_nor.copy()
            _leg = c.g_legend(_legends, legends_summary)
            _legends.append(_leg)
            _df[self.column_name] = [_leg]
            _clusters.append(_df)

        if clus_summ_axs[0]:
            return [pd.concat(_clusters)]

        if clus_summ_axs[1]:
            return _clusters

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
            # _df = c.df_value.copy() if crude else c.full_nor.copy()
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

    def g_data_checkeds_for_fig(self):
        return self.g_data_for_fig(self.g_checkeds())

    def g_data_uncheckeds_for_fig(self):
        return self.g_data_for_fig(self.g_uncheckeds())

    def g_resume_checkeds_for_fig(self):
        return self.g_resume_for_fig(self.g_checkeds())

    def g_resume_uncheckeds_for_fig(self):
        return self.g_resume_for_fig(self.g_uncheckeds())


class Cluster():
    name = ''
    shape = ''
    individuals = 0
    df_value = None
    column_name = 'Name'
    min_values = []
    max_values = []
    name_objectives = []
    full_nor = None
    df_resume_nor = None
    clus_color = None
    resu_color = None

    def __init__(self, name, shape, count, df_value, all_count, resume=None):
        self.name = name
        self.shape = shape
        self.count = count
        self.df_value = df_value
        self.all_count = all_count
        self.df_resume = self.g_resume(df_value, shape, resume)
        self.complete_max_min()

    def complete_max_min(self):
        cols = [i for i in self.df_value.columns[:-1]]
        self.max_values = self.df_value[cols].max().tolist()
        self.min_values = self.df_value[cols].min().tolist()

    def g_max_in_var(self, index):
        return self.max_values[index]

    def g_min_in_var(self, index):
        return self.min_values[index]

    def g_percent(self, total=None):
        if total is None:
            total = self.all_count
        return (self.count * 100.0) / total

    def g_percent_format(self, total=None):
        _por = self.g_percent(total)
        return str(round(_por, 2)) + '%'

    def g_percent_format_str(self, total=None):
        _por = self.g_percent(total)
        return str(round(_por, 2))

    def g_count_format(self, count=None):
        return str(self.count)

    def g_resume(self, df, shape, resume=None):

        if resume is None:
            serie_mean = df[df.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            df_mean[self.column_name] = shape
            return df_mean

        df_mean = pd.DataFrame([resume], columns=df.columns)
        return df_mean

    def g_legend(self, legends, legends_condition, repeat=False):
        _legend = ""

        if legends_condition[2]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.name

        if legends_condition[3]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + str(self.shape)
            
        if legends_condition[0]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.g_percent_format()

        if legends_condition[1]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + str(self.count)

        if not repeat:
            while _legend in legends:
                _legend = _legend + "."
        return _legend
