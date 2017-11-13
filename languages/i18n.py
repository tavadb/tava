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
# Creado:  4/8/2015                                          ###
#                                                            ###
# ##############################################################
'''
import wx
import os

ID_ES_PY_LANGUAGE = 0
ID_EN_US_LANGUAGE = 1


class I18nLocale(wx.Locale):

    def __init__(self, langua):
        wx.Locale.__init__(self, language=wx.LANGUAGE_DEFAULT)

        # verificación de archivos de internacionlización
        if os.path.exists('./locale'):
            self.path_es_py = './locale/es_PY/'
            self.file_es_py = 'tava_es_PY'
            self.path_en_us = './locale/en_US/'
            self.file_es_us = 'tava_en_US'

            # idioma español paraguay
            es_py_po = './locale/es_PY/tava_es_PY.po'
            es_py_mo = './locale/es_PY/tava_es_PY.mo'
            cmd = 'msgfmt --output-file="' + es_py_mo + '" "' + es_py_po + '"'
            os.system(cmd)

            # idioma ingles estados unidos
            en_us_po = './locale/en_US/tava_en_US.po'
            en_us_mo = './locale/en_US/tava_en_US.mo'
            cmd = 'msgfmt --output-file="' + en_us_mo + '" "' + en_us_po + '"'
            os.system(cmd)

            if langua == 'es':
                self.OnEsPy()
            else:
                self.OnEnUs()

    def SetCatalog(self, catalog):
        self.AddCatalog(catalog)

    def OnEsPy(self):
        self.language = ID_ES_PY_LANGUAGE
        self.AddCatalogLookupPathPrefix(self.path_es_py)
        self.AddCatalog(self.file_es_py)

    def OnEnUs(self):
        self.language = ID_EN_US_LANGUAGE
        self.AddCatalogLookupPathPrefix(self.path_en_us)
        self.AddCatalog(self.file_es_us)

    def isEsPyLanguage(self):
        if self.language == ID_ES_PY_LANGUAGE:
            return True
        return False

    def isEnUsLanguage(self):
        if self.language == ID_EN_US_LANGUAGE:
            return True
        return False
