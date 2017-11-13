
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)     ###
#                                                            ###
# Creado:  /10/2016                                          ###
#                                                            ###
# ##############################################################


------------------------------------------------------------------------
		TAVA - Repositorio : https://github.com/abrahanfretes/tava
		
------------------------------------------------------------------------

------------------------------------------------------------------------
		TAVA - ENTORNO DE DESARROLLO - Librerias necesarias
------------------------------------------------------------------------

----------------------------------------------
LIBRERIAS - UTILIZADAS
----------------------------------------------
(1) Build Essencial
	> sudo apt-get install build-essential

(2)-> Setuptools
	* descarga = https://pypi.python.org/pypi/setuptools/17.1.1
	* documentacion = https://pypi.python.org/pypi/setuptools/17.1.1#installation-instructions
	* procedimiento de instalación
		> tar -xzvf pypa-setuptools-65921e08c351.tar.gz
		> cd pypa-setuptools-65921e08c351/
		> sudo python setup.py install

(3)-> Numpy1.9.2
	* descarga = http://sourceforge.net/projects/numpy/files/NumPy/
	* documentacion = https://pypi.python.org/pypi/pandas/0.16.2/
	* procedimiento de instalación
		> tar -xzvf numpy-1.9.2.tar.gz
		> cd numpy-1.9.2/
		> sudo python setup.py install

(4)-> Pandas0.16.2
	* descarga = https://pypi.python.org/pypi/pandas/0.16.2/#downloads
	* documentacion = http://www.scipy.org/install.html
	* procedimiento de instalación
		> tar -xzvf pandas-0.16.2.tar.gz
		> cd pandas-0.16.2/
		> sudo python setup.py install

(5)-> Matplotlib
	* descarga = https://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.4.3/matplotlib-1.4.3.tar.gz/download
	* documentacion = http://matplotlib.org/users/installing.html
	* procedimiento de instalación
		> tar -xzvf matplotlib-1.4.3.tar.gz
		> cd matplotlib-1.4.3/
		> sudo apt-get build-dep python-matplotlib
		> sudo python setup.py install

(6)-> SCIPY
	* descarga = http://www.scipy.org/install.html
	* documentacion = http://www.scipy.org/install.html
	* procedimiento de instalación
		> sudo apt-get install python-scipy ipython ipython-notebook python-sympy python-nose

(7)-> SqlAlchemy0.9.9 
	* descarga = https://pypi.python.org/pypi/SQLAlchemy/0.9.9
	* documentacion = http://docs.sqlalchemy.org/en/rel_0_9/
	* procedimiento de instalación
		> tar -xzvf SQLAlchemy-0.9.9.tar.gz
		> cd SQLAlchemy-0.9.9/
		> sudo python setup.py install
		> respeusta final = Installed /usr/local/lib/python2.7/dist-packages/SQLAlchemy-0.9.9-py2.7-linux-x86_64.egg
			    Processing dependencies for SQLAlchemy==0.9.9
			    Finished processing dependencies for SQLAlchemy==0.9.9


(8)-> wxpython 2.9.3.1
	* descarga = http://sourceforge.net/projects/wxpython/files/wxPython/2.9.3.1/wxPython-src-2.9.3.1.tar.bz2/download
	* documentacion = http://wiki.wxpython.org/CheckInstall
	* procedimiento de instalación
		> sudo apt-get install libgtk2.0-dev libgtk2.0-doc libglu1-mesa 
		> sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev libgstreamer0.10-dev 
		> sudo apt-get install libgconf2-dev libsdl1.2-dev zlib1g-dev libjpeg62-dev 
		> sudo apt-get install libjpeg-turbo8-dev libjpeg8-dev libjpeg-dev libtiff4-dev python-gst0.10-dev
		
		> sudo apt-get install dpkg-dev swig python2.7-dev
		> sudo apt-get install libwebkitgtk-dev libtiff-dev checkinstall
		> sudo apt-get install ubuntu-restricted-extras freeglut3 freeglut3-dev
		> sudo apt-get install libgstreamer-plugins-base0.10-dev 

		> tar -xzvf wxPython-src-2.9.3.1.tar.bz2
		> cd wxPython-src-2.9.3.1/
		> mkdir bld
		> python build-wxpython.py --build_dir=../bld
		
		> #exportar la libreria (agregar en el bashcr, esto es el directorio de instalacion para que funcione el demo)
		export PYTHONPATH=$PYTHONPATH:/home/afretes/tesis/librerias/wxpython/wxPython-src-2.9.3.1/wxPython
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/afretes/tesis/librerias/wxpython/wxPython-src-2.9.3.1/bld/lib

		En Eclipse, ir hasta:
			Windows -> Preferences -> PyDev -> Interpreters -> Python Interpreter
			En la pestaña de Libraries quitar la referencia /usr/lib/python2.7/dist-packages/wx-2.8-gtk2-unicode
			Luego agregar como nueva referencia: “ubicacion”/wxPython-src-2.9.3.1/wxPython y Listo. 


(9)-> cx_Freeze-4.3.4
	* descarga = https://pypi.python.org/pypi?:action=display&name=cx_Freeze&version=4.3.4
	* documentacion = 
	* procedimiento de instalación
		> tar -xzvf cx_Freeze-4.3.4.tar.gz
		> cd cx_Freeze-4.3.4/
		> en el archivo setup.py cambiar 'not vars.get("Py_ENABLE_SHARED", 0)' por True
		> python setup.py build
		> sudo python setup.py install
