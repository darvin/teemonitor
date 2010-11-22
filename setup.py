#!/usr/bin/python
from setuptools import setup, find_packages

execfile('src/teemonitor/__init__.py')

setup(
          name = "teemonitor",
          version = __version__,
          url = 'http://github.com/darvin/teemonitor',
          license = 'GPL',
          description = "Teeworlds monitor system",
          author = 'Sergey Klimov',
          packages = find_packages('src'),
          package_dir = {'': 'src'},
          install_requires = ['setuptools'],
     )
