#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arseferreira@gmail.com)      ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  4/8/2015                                          ###
#                                                            ###
# ##############################################################
'''


# Send = wrapper->TavaMenuBAr
# Subscribe = ALL
LANGUAGE_CHANGED = 'LANGUAGE.CHANGED'

# Send = wrapper->ToolBar
# Subscribe = main->TavaFrame
NEW_PROJECT = 'NEW.PROJECT'

# Send = wrapper->ToolBar
# Subscribe = main->TavaFrame
NEW_RESULTS = 'NEW.RESULTS'

# Send = vmenu->MenuAR
# Subscribe = main->TavaFrame
DELETE_RESULT = 'DELETE.RESULTS'
CHANGE_RESULT = 'CHANGE.RESULTS'
CONGIF_RESULT = 'CONGIF.RESULTS'


# Send = vmenu->MenuAR
# Subscribe = main->TavaFrame
DELETE_RESULT_TREE = 'DELETE.RESULTS_TREE'

# Send = vmenu->MenuAR
# Subscribe = main->TavaFrame
DELETE_VIEW = 'DELETE.VIEW'
PRE_DELETE_VIEW = 'PRE.DELETE_VIEW'


# Send = vmenu->MenuAR
# Subscribe = main->TavaFrame
DELETE_VIEW_TREE = 'DELETE.VIEW_TREE'

# Send = vmenu->MenuAV
# Subscribe = main->TavaFrame
CREATE_VIEW = 'CREATE.VIEW'

# Send = wrapper->TavaTree
# Subscribe = wrapper->TavaSpaceWork
SHOW_SELECTED_VIEW = 'SHOWSELECTED.VIEW'

# Send = wrapper->ToolBar
# Subscribe = main->TavaFrame
PREUNHIDE_PROJECT = 'PREUNHIDE.PROJECT'

# Send = wrapper->ToolBar
# Subscribe = ptree->TavaTreeP
OPEN_PROJECT = 'OPEN.PROJECT'

# Send = wrapper->ToolBar
# Send = vmenu->MenuP
# Subscribe = ptree->TavaTreeP
CLOSE_PROJECT = 'CLOSE.PROJECT'

# Send = wrapper->ToolBar
# Subscribe = ptree->TavaTreeP
DELETE_PROJECT = 'DELETE.PROJECT'

# Send = wrapper->ToolBar
# Subscribe = ptree->TavaTreeP
HIDE_PROJECT = 'HIDE.PROJECT'

# Send = wrapper->ToolBar
# Subscribe = wrapper->TavaFrame
EXIT_APP = 'EXIT.APP'

# Send = main->TavaFrame
# Subscribe = ptree->TavaTreeP
ADD_PROJECT_IN_TREE = 'ADDPROJECT.INTREE'

# Send = main->TavaFrame
# Subscribe = ptree->TavaTreeP
ADD_RESULTS_IN_TREE = 'ADDRESULTS.INTREE'

# Send = main->TavaFrame
# Subscribe = ptree->TavaTreeP
ADD_VIEW_IN_TREE = 'ADDVIEW.INTREE'

# Send = vproject->UnhideProjec
# Subscribe = wrapper->TavaTree
UNHIDE_PROJECT = 'UNHIDE.PROJECT'

# Send = vmenu->MenuP
# Subscribe = main->TavaFrame
RENAME_PROJECT = 'RENAME.PROJECT'

# Send = vmenu->MenuP
# Subscribe = main->TavaFrame
PROPERTIES_PROJECT = 'PROPERTIES.PROJECT'

# Send = pproject
# Subscribe = ptree
PROJECT_UPDATE = 'PROJECT.UPDATE'

# Send = wrapper->ToolBar
# Subscribe = main->TavaFrame
PRE_EXIT_APP = 'PRE_EXIT.APP'

# Send = ptree->ToolBar->TavaTreeP->selected_project
# Subscribe = wrapper->TavaToolBar
# Subscribe = ptree->TavaTreeP
TYPE_CHANGED_SELECTED_PROJECT = 'TYPE_CHANGED_SELECTED_PROJECT'
TYPE_CHANGED_UNSELECTED_PROJECT = 'TYPE_CHANGED_UNSELECTED_PROJECT'

# Send = vmenu->MenuResultMetric
# Subscribe = main->TavaFrame
ADD_RESULT_METRIC = 'ADD.RESULT_METRIC'

# Send = vmenu->MenuFileResultMetric
# subscribe = wrapper->TavaSpaceWork
OPEN_RESULT_METRIC = 'OPEN.RESULT_METRIC'

# Send = pmetric->MainPanelPresenter
# Subscribe = ptree->TavaTreeP
ADD_RESULT_METRIC_IN_TREE = 'ADD_IN_TREE.RESULT_METRIC'

# Send = vcontrol -> ControlPanel
# Subscribe = main->MainFrame
START_BUSY = 'START_BUSY'

# Send = vcontrol -> ControlPanel, vfigure->FigurePanel
# Subscribe = main->MainFrame
STOP_BUSY = 'STOP_BUSY'
