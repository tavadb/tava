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
# Creado:  18/2/2016                                         ###
#                                                            ###
# ##############################################################
'''
from bd.entity import Result, Iteration, Individual
from exception.tava_exception import ParserError
from resources.tava_path import tava_base_name


# cabeceras de archivo tava
RESULTNAME = '*RESULTNAME:'
ALGORITHMS = '*ALGORITHMS:'
NOTES = '*NOTES:'
RUNSSTORE = '*RUNSSTORE:'
MAXPOPULATION = '*POPULATIONMAX:'
OBJECTIVESNAMES = '*OBJECTIVESNAMES:'
VARIABLESNAMES = '*VARIABLESNAMES:'
OBJECTIVES = '*OBJECTIVES:'
VARIABLES = '*VARIABLES:'

# cabeceras de iteraciones archivo tava
IDITERATION = '*IDITERATION:'
TIMEPROCESS = '*TIMEPROCESS:'
INDIVIDUAL = '*INDIVIDUAL:'


class TavaFileToResult():
    '''

    '''

    def __init__(self, f_tava):
        self.result = Result()
        self.c_line = 0
        self.all_headers = {}
        self.f_tava = f_tava
        self.size_header = 0
        pass

    def make_parsing(self, m_tit, dlg):

        try:
            self.header_processing()
            dlg.UpdatePulse(m_tit + '.')
            self.add_atributes()
            dlg.UpdatePulse(m_tit + '..')
            self.add_iterations(m_tit, dlg)
        except IOError as ioerror:
            self.value_error("Error IOError: {0}".format(ioerror))
        except IndexError as indexerror:
            self.value_error("Error IndexError: {0}".format(indexerror))
        except ValueError as valueerror:
            self.value_error("Error ValueError: {0}".format(valueerror))
#         except Exception as e:
#             self.value_error("Error Exception: {0}".format(e))

    def add_iterations(self, m_tit, dlg):

        with open(self.f_tava, 'r') as f_tava:

            _mps = '.'
            # lectura de cabeceras no necesarias
            self.c_line = self.size_header-3
            [f_tava.readline() for _ in range(self.size_header-3)]

            # iteraciones
            _its = []
            for _ in range(self.result.runstore):
                i_h = []
                self.c_line += 1
                i_h.append(f_tava.readline())
                self.c_line += 1
                i_h.append(f_tava.readline())
                self.c_line += 1
                i_h.append(f_tava.readline())

                _h = [h.strip().split(':') for h in i_h]

                # atributos
                _it = Iteration()
                _it.number = int(_h[0][1])
                _it.individual = int(_h[1][1])
                _it.run_time = float(_h[2][1])

                # individuos
                _ins = []
                for i_num in range(_it.individual):
                    self.c_line += 1
                    o, _, _ = self.g_individuals(f_tava.readline().strip())

                    # atributos
                    _in = Individual()
                    _in.number = i_num + 1
                    _in.objectives = o
                    # _in.variables = v
                    # _in.var_dtlz = d
                    _ins.append(_in)

                _it.individuals = _ins
                _its.append(_it)

                dlg.UpdatePulse(m_tit + '\n' + _mps)
                _mps = _mps + '.'

            self.result.iterations = _its

    def g_individuals(self, str_indi):
        '''
        Verifica que los valores o individuos cumplen con los tipos de datos
        necesarios.

        :param str_indi:
        :type str_indi:
        '''
        str_o, str_v, str_z = str_indi.split(';')

        # prueba de objetivos
        try:
            [float(o) for o in str_o.split(',')]
        except:
            _obj = [str(float.fromhex(o)) for o in str_o.split(',')]
            str_o = ','.join(_obj)

        # prueba de variables
        try:
            [float(v) for v in str_v.split(',')]
        except:
            _var = [str(float.fromhex(v)) for v in str_v.split(',')]
            str_v = ','.join(_var)

        # prueba de dtlz
        try:
            str_z = float(str_z)
        except:
            str_z = float.fromhex(str_z)

        return str_o, str_v, str_z

    def header_processing(self):
        with open(self.f_tava, 'r') as f_tava:

            # extrayendo cabecera

            self.c_line += 1
            lineread = f_tava.readline().strip()
            while lineread[0] == '*':
                self.size_header += 1
                # ValueError: too many values to unpack
                key, value = lineread.split(':')
                self.all_headers[key+':'] = value
                self.c_line += 1
                lineread = f_tava.readline().strip()

            # comprobando minima cantidad de cabeceras
            if self.size_header < 6:
                raise ParserError(self.f_tava,
                                  'Faltan minimas obligatorias')

            # comprobando cabeceras obligatorias
            for value in [RUNSSTORE, OBJECTIVES, VARIABLES]:
                if not(value in self.all_headers.keys()):
                    raise ParserError(self.f_tava,
                                      'Faltan cabeceras obligatorias')

            # comprobando cabeceras obligatorias
            for value in [IDITERATION, INDIVIDUAL, TIMEPROCESS]:
                if not(value in self.all_headers.keys()):
                    raise ParserError(self.f_tava,
                                      'Faltan cabeceras obligatorias')

    def add_atributes(self):
        all_headers = self.all_headers
        # atributos, obligatorios
        self.result.runstore = int(all_headers[RUNSSTORE])
        self.result.objectives = int(all_headers[OBJECTIVES])
        self.result.variables = int(all_headers[VARIABLES])

        # atributos, calculados si no encontrados
        if RESULTNAME in all_headers.keys():
            self.result.name = all_headers[RESULTNAME]
            self.result.alias = all_headers[RESULTNAME]
        else:
            self.result.name = tava_base_name(self.f_tava)
            self.result.alias = tava_base_name(self.f_tava)

        if OBJECTIVESNAMES in all_headers.keys():
            self.result.name_objectives = all_headers[OBJECTIVESNAMES]
        else:
            c = self.result.objectives
            n_objs = ','.join(['O'+str(i+1) for i in range(c)])
            self.result.name_objectives = n_objs

        if VARIABLESNAMES in all_headers.keys():
            self.result.name_variables = all_headers[VARIABLESNAMES]
        else:
            c = self.result.objectives
            n_vars = ','.join(['V'+str(i+1) for i in range(c)])
            self.result.name_variables = n_vars

        # atributos, opcionales
        if NOTES in all_headers.keys():
            self.result.notes = all_headers[NOTES]
        if ALGORITHMS in all_headers.keys():
            self.result.algorithms = all_headers[ALGORITHMS]
        if MAXPOPULATION in all_headers.keys():
            self.result.populationmax = int(all_headers[MAXPOPULATION])

    def value_error(self, message):
        raise ParserError(self.f_tava, message, self.c_line)


class SepFileToResult():
    '''

    '''

    def __init__(self, f_tava):
        self.result = Result()
        self.f_tava = f_tava

    def make_parsing(self, m_tit, sep, dlg):

        try:
            dlg.UpdatePulse(m_tit + '.')

            # ---- verificar cantidad de iteraciones - creación de blocks
            # ---- se toman como bloques aquellos valores divididos en
            # ----  lineas blancas
            blocks = []
            with open(self.f_tava, 'r') as f_tava:
                datas = [l.strip() for l in f_tava.readlines()]
                if datas.count('') > 0:
                    while datas != []:
                        datas = self.clean_init(datas)
                        if datas.count('') > 0:
                            index = datas.index('')
                            blocks.append(datas[0:index])
                            datas = datas[index:]
                        elif datas != []:
                            blocks.append(datas)
                            datas = []
                else:
                    blocks.append(datas)

            # ---- verificar separador
            # ---- se verifica si contiene el separador apropiado, seleccionado
            # ---- en la vista como separador actual
            # ---- verificar catidad de objetivos iguales
            count_objetives = []
            for bs in blocks:
                for ind in bs:
                    objs = ind.count(sep)
                    if objs < 1:
                        # ---- error
                        mess = "Error de Formato, el separador ' " \
                            + sep + " ' no es correcto."
                        self.value_error(mess)

                    if count_objetives != [] and not (objs in count_objetives):
                        mess = "Error de Formato, cantidad de objetivos " + \
                            "desiguales."
                        self.value_error(mess)
                    count_objetives.append(objs)

            # ----
            # ---- completar atributos de results
            # ----

            self.result.runstore = len(blocks)
            # self.result.objectives = int(all_headers[OBJECTIVES])
            # self.result.variables = int(all_headers[VARIABLES])
            self.result.name = tava_base_name(self.f_tava)
            self.result.alias = tava_base_name(self.f_tava)
            # self.result.name_variables = all_headers[VARIABLESNAMES]

            _its = []
            _mps = '.'
            for bs in blocks:

                # ---- creación de iteraciones
                _it = Iteration()
                _it.number = 1

                # ---- creación de individuos
                _ins = []
                _count_objec = 0

                for i_num, line in enumerate(bs):
                    indi = line.split(sep)
                    _in = Individual()
                    _in.number = i_num + 1
                    _in.objectives = self.g_individuals(indi)
                    _ins.append(_in)
                    _count_objec = len(indi)

                    dlg.UpdatePulse(m_tit + '\n' + _mps)
                    _mps = _mps + '.'
                    _mps = '.' if len(_mps) == 5 else _mps

                _it.individual = len(_ins)
                _it.individuals = _ins
                _its.append(_it)

            # ---- agregación de resultado
            self.result.iterations = _its
            self.result.objectives = _count_objec
            n_objs = ','.join([str(_i) for _i in range(_count_objec)])
            self.result.name_objectives = n_objs

        except IOError as ioerror:
            self.value_error("Error IOError: {0}".format(ioerror))
        except IndexError as indexerror:
            self.value_error("Error IndexError: {0}".format(indexerror))
        except ValueError as valueerror:
            self.value_error("Error ValueError: {0}".format(valueerror))
#         except Exception as e:
#             self.value_error("Error Exception: {0}".format(e))

    def g_individuals(self, indi):
        '''
        Verifica que los valores o individuos cumplen con los tipos de datos
        necesarios.

        :param str_indi:
        :type str_indi:
        '''

        # ---- verificación del individuo float o exade
        try:
            [float(o) for o in indi]
            str_o = ','.join(indi)
        except:
            str_o = ','.join([str(float.fromhex(o)) for o in indi])

        return str_o

    def value_error(self, message):
        raise ParserError(tava_base_name(self.f_tava), message, 0)

    def clean_init(self, _list):
        while _list != [] and _list[0] == '':
            _list.remove('')
        return _list
