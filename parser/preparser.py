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
# Creado:  19/2/2016                                         ###
#                                                            ###
# ##############################################################
'''
from exception.tava_exception import PreParserError
from parser.tavaparser import IDITERATION, INDIVIDUAL, TIMEPROCESS, RESULTNAME,\
    ALGORITHMS, NOTES, RUNSSTORE, MAXPOPULATION, OBJECTIVESNAMES, VARIABLESNAMES,\
    OBJECTIVES, VARIABLES
from resources.tava_path import new_tava_file, tava_base_name


MAX_SEARCH_HEAER = 30


class VonToTavaParser():

    '''

    '''

    def __init__(self, file_von, dir_parsed):
        self.f_von = file_von
        self.dir_parsed = dir_parsed
        self.c_line = 0
        self.runstore = 0
        self.algorithm = ''
        self.notes = []
        self.objectives = 0
        self.variables = 0
        self.max_populations = 0

        self.size_header = 0
        self.init_time = 0.0
        self.init_individuals = 0

    def make_preparsing(self, m_tit, dlg):

        try:
            # procesar valores de cabecera
            self.header_processing()
            dlg.UpdatePulse(m_tit + '.')
            # procesar iteraciones y creación de nuevo archivo
            tava_path = self.create_tava_file(m_tit, dlg)
        except IOError as ioerror:
            self.value_error("Error IOError: {0}".format(ioerror))
        except IndexError as indexerror:
            self.value_error("Error IndexError: {0}".format(indexerror))
        except ValueError as valueerror:
            self.value_error("Error ValueError: {0}".format(valueerror))
        except Exception as e:
            self.value_error("Error Exception: {0}".format(e))

        return tava_path

    def create_tava_file(self, m_tit, dlg):
        path_file_tava = new_tava_file(self.dir_parsed, self.f_von)
        _mps = '.'
        with open(path_file_tava, 'w') as f_tava:

            # agrega la cabecera al nuevo archivo
            for h_value in self.create_header():
                f_tava.write(h_value)

            with open(self.f_von, 'r') as f_von:

                # posicionar el puntero en un lugar correcto
                # no tener encuenta cabecera
                [str(l) + f_von.readline() for l in range(self.size_header)]
                self.c_line = int(self.size_header)

                # por la catidad de ejecuciones menos
                self.c_line += 1
                i_time = float(f_von.readline().strip())
                for c_run in range(self.runstore):

                    # lectura de una iteracion completa
                    self.c_line += 1
                    c_indis = int(f_von.readline().strip())

                    # individuos preparacion
                    indis = [f_von.readline() for _ in range(c_indis)]
                    l_indis = self.g_indi_to_lines(indis)

                    # tiempo de procesamiento preparacion
                    self.c_line += 1
                    f_time = float(f_von.readline())
                    # en la ultima iteración eltiempo de
                    # proceso se guarda diferente
                    if c_run + 1 == self.runstore:
                        self.c_line += 1
                        f_time = float(f_von.readline())
                    t_time = str(f_time - i_time)

                    # escritura de una iteracion
                    _indi = indis[0].strip().split('\t')
                    f_tava.write(IDITERATION + _indi[0] + '\n')
                    f_tava.write(INDIVIDUAL + str(c_indis) + '\n')
                    f_tava.write(TIMEPROCESS + t_time + '\n')
                    f_tava.writelines(l_indis)

                    # estableces valor de tiempo de proceso
                    i_time = int(f_time)
                    dlg.UpdatePulse(m_tit + '\n' + _mps)
                    _mps = _mps + '.'

        return path_file_tava

    def g_indi_to_lines(self, individuals):
        ret = []
        pf_var = 2 + self.variables
        pf_obj = pf_var + self.objectives
        for indi in individuals:
            self.c_line += 1
            indi = indi.strip().split('\t')

            self.verific_indi(indi[pf_var:pf_obj], indi[2:pf_var],
                              (indi[pf_obj:pf_obj + 1])[0])

            ret.append(','.join(indi[pf_var:pf_obj]) + ';' +
                       ','.join(indi[2:pf_var]) + ';' +
                       ','.join(indi[pf_obj:pf_obj + 1]) + '\n')
        return ret

    def verific_indi(self, objectives, variables, dtlz):
        '''
        Verifica que los valores o individuos cumplen con los tipos de datos
        necesarios.

        '''

        # prueba de objetivos
        try:
            [float(o) for o in objectives]
        except:
            [float.fromhex(o) for o in objectives]

        # prueba de variables
        try:
            [float(v) for v in variables]
        except:
            [float.fromhex(v) for v in variables]

        # prueba de dtlz
        try:
            float(dtlz)
        except:
            float.fromhex(dtlz)

    def create_header(self):
        ret = []
        ret.append(RESULTNAME + tava_base_name(self.f_von) + '\n')
        ret.append(ALGORITHMS + self.algorithm + '\n')
        ret.append(NOTES + ' '.join(self.notes) + '\n')
        ret.append(RUNSSTORE + str(self.runstore) + '\n')
        ret.append(MAXPOPULATION + str(self.max_populations) + '\n')
        n_objs = ','.join(['O' + str(i + 1) for i in range(self.objectives)])
        ret.append(OBJECTIVESNAMES + n_objs + '\n')
        n_vars = ','.join(['V' + str(i + 1) for i in range(self.variables)])
        ret.append(VARIABLESNAMES + n_vars + '\n')
        ret.append(OBJECTIVES + str(self.objectives) + '\n')
        ret.append(VARIABLES + str(self.variables) + '\n')
        return ret

    def header_processing(self):
        values_header = []
        with open(self.f_von, 'r') as f_von:

            is_header = False
            while not is_header and MAX_SEARCH_HEAER != self.c_line:
                self.c_line += 1

                values_header.append(f_von.readline().strip())

                if len(values_header) > 4:
                    try:
                        self.objectives = int(values_header[-5])
                        self.variables = int(values_header[-4])
                        self.maxi_populations = int(values_header[-3])
                        self.init_time = float(values_header[-2])
                        self.init_individuals = int(values_header[-1])
                    except ValueError:
                        pass
                    else:
                        try:
                            self.runstore = int(values_header[0])
                            self.algorithm = values_header[1]
                            self.notes = values_header[
                                2:len(values_header) - 5]
                            self.size_header = len(values_header) - 2
                        except ValueError:
                            self.value_error('Formato de' +
                                             'Cabecera incompatible')
                        is_header = True

                if MAX_SEARCH_HEAER == self.c_line:
                    self.value_error('Formato de Cabecera incompatible')

    def value_error(self, message):
        raise PreParserError(self.f_von, message, self.c_line)
