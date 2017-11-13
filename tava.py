#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)     ###
#                                                            ###
# Creado:  26/8/2016                                         ###
#                                                            ###
# ##############################################################
'''


import wx

from views.main import SplashFrame


class TavaiApp(wx.App):

    def OnInit(self):

        splash = SplashFrame()
        splash.Center(wx.BOTH)
        splash.Show()
        return True

app = TavaiApp(redirect=False)
app.MainLoop()
