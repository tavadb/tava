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
# Creado:  13/03/2016                                        ###
#                                                            ###
# ##############################################################
'''


from bd.engine import getSession
from bd.entity import ResultMetric, PropertyName, MandatoryProperties,\
    PropertyValue


def parse_csv(path, filename, delimiters, project):
    '''
    Metodo encargado de parsear y persistir los datos en el archivo de
    resultado de metricas.
    :param path: path del archivo en el file_system.
    :param filename: nombre del archivo.
    :param delimiters: String de delimitadores para el parseo.
    :param project: referencia a la instancia de proyecto asociado.
    '''
    from time import time
    _times = []

    rm = ResultMetric()
    rm.filename = filename
    rm.path = path
    rm.project_id = project.id

    getSession().add(rm)
    getSession().commit()

    total_ini = time()

    with open(path, 'r') as file_metric:

        ciclo = 1
        line = file_metric.readline().strip()

        linea_vector = parse_line(line, delimiters)
        list_properties_names = []
        properties_names_index = {}
        mandatory_properties = ["METRIC", "ITERATION", "VALUEMETRIC"]
        for idx, property_name in enumerate(linea_vector):
            pn = PropertyName(property_name)
            pn.result_metric_id = rm.id
            list_properties_names.append(pn)
            if property_name in mandatory_properties:
                properties_names_index[property_name] = idx

        getSession().add_all(list_properties_names)
        getSession().commit()

#       Leemos otra linea
        line = file_metric.readline().strip()

        ind = 1

        start_time = time()

        ii = 0

        list_mandatory_properties = []

        while line != '':
            ii += 1

            linea_vector = parse_line(line, delimiters)

#            De una linea extraemos los valores obligatorios y los guardamos en
#            la tabla mandatory_properties
            mp = MandatoryProperties()
            mp.iteration = linea_vector[properties_names_index["ITERATION"]]
            mp.metric_name = linea_vector[properties_names_index["METRIC"]]
            mp.metric_value = \
                linea_vector[properties_names_index["VALUEMETRIC"]]

            list_properties_values = []
            for idx, value in enumerate(linea_vector):
                if idx not in properties_names_index.values():
                    pv = PropertyValue(value)
                    pv.property_name_id = list_properties_names[idx].id
                    list_properties_values.append(pv)

            mp.properties_values = list_properties_values

            list_mandatory_properties.append(mp)

            if ind == 3:
                print("se procesaron tres individuos")
                break

            if ind == 25000:
                getSession().add_all(list_mandatory_properties)

                getSession().commit()

                elapsed_time = time() - start_time
                print 'time = ' + str(elapsed_time)
                _times.append(elapsed_time)
                start_time = time()
                list_mandatory_properties = []
                ciclo += 1
                ind = 0

            line = file_metric.readline().strip()
            ind += 1

        print 'fin lectura'

    if list_mandatory_properties != []:
        getSession().add_all(list_mandatory_properties)
        getSession().commit()

    total_final = time()
    print 'Total tiempo transcurrido: ' + str(total_final - total_ini)
    print _times

    return rm


def parse_line(line, delimiters):
    '''
    Metodo que realiza un split a la linea en base a los caracteres contenidos
    en la cadena de delimitadores.
    :param line: linea a ser dividida.
    :param delimiters: Cadena de delimitadores.
    '''
    for delim in delimiters:
        if delim != '.':
            line = line.replace(delim, ' ')
    return line.split(' ')
