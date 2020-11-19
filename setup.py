#!/usr/bin/env python

from setuptools import setup

setup(name='fasp',
      version='1.0',
      packages=['fasp',
                'fasp.runner',
                'fasp.search',
                'fasp.loc',
                'fasp.workflow'],
      package_data={'fasp': ['data/onek_drs.txt']},
      )