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

from wx import GetTranslation as L

from bd.entity import Project, View, ViewResult, ViewIteration
from exception.tava_exception import PreParserError, ParserError
from models.mproject import ProjectM
from models.mresult import ResultModel
from models.mview import ViewM, ViewResultM
from parser.preparser import VonToTavaParser
from parser.tavaparser import TavaFileToResult, SepFileToResult
from resources.tava_path import tava_dir_parsed, tava_dir_temp


FORMAT_TAVA = 0
FORMAT_OBJETIVE = 1


class MainFrameP(object):

    '''
    classdocs
    '''

    def __init__(self, iview):
        '''
        Constructor
        '''
        self.dir_parser = tava_dir_parsed(tava_dir_temp())
        self.iview = iview

    def add_project(self, name):
        project = ProjectM().add(Project(name))
        return project

    def add_views(self, view_name, vews_results, project):

        view = View()
        view.name = view_name
        view.project_id = project.id

        for r in vews_results:
            view_result = ViewResult()
            view_result.result_id = r.result.id
            for i in r.iterations:
                view_iteration = ViewIteration()
                if i.check:
                    view_iteration.iteration_id = i.iteration.id
                    view_result.iterations.append(view_iteration)
            view.results.append(view_result)
        if vews_results:
            _e_s = [str(i) for i in range(vews_results[0].result.objectives)]
            view.enable_sorted = ','.join(_e_s)

        return ViewM().add(view)

    def delete_view(self, view):
        ViewM().delete(view)
        return True

    def add_res(self, project, path_files, t_format, sep, dlg=None):

        results = []
        parse_correct = []
        parse_error = []
        result_names = []

        for r in project.results:
            result_names.append(r.name)

        # ---- verificar nombres repetidos

        for _p in path_files:
            if _p[1] in result_names:
                _l = 'El proyecto ya contiene mismo nombre de archivos'
                ParserError(_p[1], _l, 0)
                path_files.remove(_p)

        if FORMAT_TAVA == t_format:

            files_von_parsed = []

            # parsear archivos
            _all = len(path_files)

            for i, p in enumerate(path_files):

                m_lit = '\t' + L('MSG_PRO_FORMATER')
                m_num = ': ' + str(i + 1) + '/' + str(_all)
                m_tit = m_lit + m_num
                keepGoing = dlg.UpdatePulse(m_tit)

                try:
                    vtot = VonToTavaParser(p[0], self.dir_parser)
                    file_parsed = vtot.make_preparsing(m_tit, dlg)
                except PreParserError as preherror:
                    parse_error.append(preherror)
                else:
                    files_von_parsed.append(file_parsed)

            # crear resultdos a partir de archivos preparseados
            for i, tava_file in enumerate(files_von_parsed):

                m_lit = '\t' + L('MSG_PRO_PARSER')
                m_num = ': ' + str(i + 1) + '/' + str(_all)
                m_tit = m_lit + m_num
                keepGoing = dlg.UpdatePulse(m_tit)

                try:
                    tfr = TavaFileToResult(tava_file)
                    tfr.make_parsing(m_tit, dlg)
                except ParserError as parseerror:
                    parse_error.append(parseerror)
                else:
                    try:
                        m_lit = '\t' + L('MSG_PRO_SAVE')
                        m_tit = m_lit + m_num
                        keepGoing = dlg.UpdatePulse(m_tit)

                        # agrega a la base de datos
                        tfr.result.project_id = project.id
                        _iterations = list(tfr.result.iterations)
                        result = tfr.result
                        result.iterations = []
                        result = ResultModel().add(result)

                        _ite_all = len(_iterations)
                        for ii, ite in enumerate(_iterations):
                            m_lit_b = '\n' + L('MSG_PRO_DATA_SAVE')
                            m_num_b = ': ' + str(ii + 1) + '/' + str(_ite_all)
                            m_tit_b = m_tit + m_lit_b + m_num_b
                            keepGoing = dlg.UpdatePulse(m_tit_b)

                            result.iterations.append(ite)
                            result = ResultModel().update_init(result)
                            if not keepGoing:
                                dlg.UpdatePulse('Aborting')
                                return results

                    except Exception as e:
                        p_e = ParserError(tava_file,
                                          "Error Exception: {0}".format(e),
                                          None)
                        parse_error.append(p_e)
                    else:
                        results.append(result)
                        parse_correct.append(object)

        elif FORMAT_OBJETIVE == t_format:
            _all = len(path_files)
            for i, p in enumerate(path_files):

                try:
                    m_lit = '\t' + L('MSG_PRO_PARSER')
                    m_num = ': ' + str(i + 1) + '/' + str(_all)
                    m_tit = m_lit + m_num
                    keepGoing = dlg.UpdatePulse(m_tit)

                    tfr = SepFileToResult(p[0])
                    tfr.make_parsing(m_tit, sep, dlg)

                except ParserError as parseerror:
                    parse_error.append(parseerror)
                else:
                    m_lit = '\t' + L('MSG_PRO_SAVE')
                    m_tit = m_lit + m_num
                    keepGoing = dlg.UpdatePulse(m_tit)

                    # agrega a la base de datos
                    tfr.result.project_id = project.id
                    _iterations = list(tfr.result.iterations)
                    result = tfr.result
                    result.iterations = []
                    result = ResultModel().add(result)

                    _ite_all = len(_iterations)
                    for ii, ite in enumerate(_iterations):
                        m_lit_b = '\n' + L('MSG_PRO_DATA_SAVE')
                        m_num_b = ': ' + str(ii + 1) + '/' + str(_ite_all)
                        m_tit_b = m_tit + m_lit_b + m_num_b
                        keepGoing = dlg.UpdatePulse(m_tit_b)

                        result.iterations.append(ite)
                        result = ResultModel().update_init(result)
                        if not keepGoing:
                            dlg.UpdatePulse('Aborting')
                            return results

                    results.append(result)
                    parse_correct.append(object)

        elif 10 == t_format:

            # crear resultdos a partir de archivos preparseados
            for tava_file in path_files:
                try:
                    tfr = TavaFileToResult(tava_file)
                    tfr.make_parsing()
                except ParserError as parseerror:
                    parse_error.append(parseerror)
                else:
                    try:
                        # agrega a la base de datos
                        tfr.result.project_id = project.id
                        result = ResultModel().add(tfr.result)
                    except Exception as e:
                        p_e = ParserError(tava_file,
                                          "Error Exception: {0}".format(e),
                                          None)
                        parse_error.append(p_e)
                    else:
                        results.append(result)
                        parse_correct.append(object)

        return results, parse_error

    def contain_view(self, result_id):
        return ViewResultM().use_in_viste(result_id)

    def delete_result(self, result):
        ResultModel().delete(result)
        return True
    
    def update_result(self, result):
        ResultModel().update(result)
        return True
