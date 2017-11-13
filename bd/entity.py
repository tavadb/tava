#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingeniería en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)     ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  4/8/2015                                          ###
#                                                            ###
# ##############################################################
'''

from sqlalchemy import SmallInteger, Text, ForeignKey, Float
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from engine import Base, createDataDase


class Project(Base):
    '''
    '''

    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    blog = Column(Text(2000), nullable=True)
    state = Column(SmallInteger, nullable=False)
    creation = Column(Date(), nullable=False)
    occultation = Column(Date(), nullable=True)
    proj_open = Column(Boolean, nullable=False)
    pack_file = Column(Boolean, nullable=False)
    pack_view = Column(Boolean, nullable=False)

    results = relationship('Result', lazy=True,
                           cascade="save-update, merge, delete",
                           order_by='Result.id', backref='project')

    views = relationship('View', lazy=True,
                         cascade="save-update, merge, delete",
                         order_by='View.id', backref='project')

    results_metrics = relationship('ResultMetric', lazy=True,
                                   cascade="save-update, merge, delete",
                                   order_by='ResultMetric.id',
                                   backref='project')

    def __init__(self, name, blog=None, state=None, date=None,
                 proj_open=True, pack_file=False, pack_view=False):

        self.name = name
        self.blog = blog
        self.state = state
        self.creation = date
        self.proj_open = proj_open
        self.pack_file = pack_file
        self.pack_view = pack_view

    def __repr__(self):
        return "<Project(name='%s', blog='%s', state='%s',\
        creation_date='%s')>" % (self.name, self.blog,
                                 self.state, self.creation)


class Result(Base):
    '''
    '''
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100))
    alias = Column(String(100))

    notes = Column(String(200))
    algorithms = Column(String(100))
    populationmax = Column(Integer)
    runstore = Column(Integer)
    objectives = Column(Integer)
    variables = Column(Integer)

    name_objectives = Column(String(100))
    name_variables = Column(String(100))
    creation = Column(Date())
    update = Column(Date())
    project_id = Column(Integer, ForeignKey('project.id'))

    iterations = relationship('Iteration', lazy=True,
                              cascade="save-update, merge, delete",
                              order_by='Iteration.id', back_populates='result')

    view_results = relationship("ViewResult", back_populates="result",
                                lazy=True)

    def __init__(self):
        pass

    def __repr__(self):
        return "<Result(id='%s',name='%s',alias='%s',notes='%s',\
        algorithms='%s', populationmax='%s', runstore='%s',\
        objectives='%s',variables='%s', name_objectives='%s',\
        name_variables='%s',creation='%s', update='%s',\
        project_id='%s')>"\
        % (self.id, self.name, self.alias, self.notes, self.algorithms,
           self.populationmax, self.runstore, self.objectives, self.variables,
           self.name_objectives, self.name_variables, self.creation,
           self.update, self.project_id)


class Iteration(Base):
    ''''''

    __tablename__ = 'iteration'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    number = Column(Integer)
    individual = Column(Integer)
    run_time = Column(Float)
    result_id = Column(Integer, ForeignKey('result.id'))

    result = relationship("Result", back_populates="iterations")

    view_iterations = relationship("ViewIteration", back_populates="iteration",
                                   lazy=True)

    individuals = relationship('Individual', lazy=True,
                               cascade="save-update, merge, delete",
                               order_by='Individual.id', backref='iteration')

    def __init__(self):
        pass

    def __repr__(self):
        return "<Iteration(id:'%s',number:'%s',individual:'%s',run_time:'%s',\
        result_id:'%s')>" % (self.id, self.identifier, self.number,
                             self.individual, self.run_time, self.result_id)


class Individual(Base):
    ''''''

    __tablename__ = 'individual'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    number = Column(Integer)
    objectives = Column(String(500))
    variables = Column(String(500))
    var_dtlz = Column(Float)

    iteration_id = Column(Integer, ForeignKey('iteration.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<Individual(id:'%s',number:'%s',objectives:'%s',\
        variables:'%s',var_dtlz:'%s')>" % (self.id, self.number,
                                           self.objectives, self.variables,
                                           self.var_dtlz)


class View(Base):
    ''''''

    __tablename__ = 'view'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    description = Column(Text(2000), nullable=True)
    creation = Column(Date(), nullable=False)
    update = Column(Date())
    project_id = Column(Integer, ForeignKey('project.id'))
    enable_sorted = Column(String(150))

    wiht_grid = Column(Boolean, nullable=False)
    wiht_legend = Column(Boolean, nullable=False)
    wiht_xvline = Column(Boolean, nullable=False)
    columns_axis = Column(Integer, nullable=False)

    results = relationship('ViewResult', lazy=True,
                           cascade="save-update, merge, delete",
                           order_by='ViewResult.id', backref='view')

    def __init__(self):
        pass

    def __repr__(self):
        return "<View(name='%s', description='%s', creation='%s,\
                enable_sorted='%s')>" % (self.name, self.description,
                                         self.creation, self.enable_sorted)

    def __eq__(self, view):
        if self.name != view.name:
            return False
        if self.description != view.description:
            return False
        if self.creation != view.creation:
            return False
        if self.enable_sorted != view.enable_sorted:
            return False
        if self.wiht_grid != view.wiht_grid:
            return False
        if self.wiht_legend != view.wiht_legend:
            return False
        if self.wiht_xvline != view.wiht_xvline:
            return False
        if self.columns_axis != view.columns_axis:
            return False

        return True

    def __ne__(self, view):
        if self.name != view.name:
            return True
        if self.description != view.description:
            return True
        if self.creation != view.creation:
            return True
        if self.enable_sorted != view.enable_sorted:
            return True
        if self.wiht_grid != view.wiht_grid:
            return True
        if self.wiht_legend != view.wiht_legend:
            return True
        if self.wiht_xvline != view.wiht_xvline:
            return True
        if self.columns_axis != view.columns_axis:
            return True

        return False


class ViewResult(Base):
    ''''''

    __tablename__ = 'view_result'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    view_id = Column(Integer, ForeignKey('view.id'))
    result_id = Column(Integer, ForeignKey('result.id'))

    result = relationship("Result", back_populates="view_results")

    iterations = relationship('ViewIteration', lazy=True,
                              cascade="save-update, merge, delete",
                              order_by='ViewIteration.id',
                              backref='view_result')

    def __init__(self):
        pass

    def __repr__(self):
        return "<ViewData(id='%i')>" % (self.id)


class ViewIteration(Base):
    ''''''

    __tablename__ = 'view_iteration'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    view_result_id = Column(Integer, ForeignKey('view_result.id'))
    iteration_id = Column(Integer, ForeignKey('iteration.id'))

    iteration = relationship("Iteration", back_populates="view_iterations")

    def __init__(self):
        pass

    def __repr__(self):
        return "<ViewIteration(id='%s')>" % (self.id)


class SomConfig(Base):
    '''
    Entidad que alberga las configuraciones realizadas a una visualizacion
    del tipo SOM.
    '''

    __tablename__ = 'som_config'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    learning_rate = Column(Float)
    sigma = Column(Float)
    topology = Column(String(20))
    columns = Column(Integer)
    rows = Column(Integer)
    map_initialization = Column(String(20))
    neighborhood = Column(String(50))
    iterations = Column(Integer)
    view_id = Column(Integer, ForeignKey('view.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<SomConfig()>"


class ResultMetric(Base):
    '''
    Mapeado de la tabla result_metric.
    '''

    __tablename__ = 'result_metric'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    filename = Column(String(100))
    path = Column(String(100))
    project_id = Column(Integer, ForeignKey('project.id'))

    def __init__(self):
        pass

    def __repr__(self):
        return "<ResultMetric()>"


class PropertyName(Base):
    '''
    Mapeado de la tabla property_name.
    '''

    __tablename__ = 'property_name'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    result_metric_id = Column(Integer, ForeignKey('result_metric.id'))

    def __init__(self, name):
        self.name = name


class MandatoryProperties(Base):
    '''
    Mapeado de la tabla mandatory_properties.
    '''

    __tablename__ = 'mandatory_properties'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    iteration = Column(String(100), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(String(100), nullable=False)

    properties_values = relationship('PropertyValue', lazy=True,
                                     cascade="save-update, merge, delete",
                                     order_by='PropertyValue.id',
                                     back_populates='mandatory_properties')


class PropertyValue(Base):
    '''
    Mapeado de la tabla property_value.
    '''

    __tablename__ = 'property_value'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    value = Column(String(100), nullable=False)
    property_name_id = Column(Integer, ForeignKey('property_name.id'))
    mandatory_properties_id = Column(Integer,
                                     ForeignKey('mandatory_properties.id'))
    mandatory_properties = relationship("MandatoryProperties",
                                        back_populates="properties_values")

    def __init__(self, value):
        self.value = value


def createDB():
    createDataDase()
