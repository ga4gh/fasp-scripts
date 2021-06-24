#!/usr/bin/env python

from setuptools import setup

install_requires = [
    'applescript',
    'google-api-python-client',
    'google-cloud-bigquery',
    'google-cloud-storage',
    'ipykernel',
    'notebook',
    'oauth2client',
    'pandas',
    'Pillow',
    'pyega3',
    'requests',
    'sevenbridges-python',
    'humanize'
]

setup(name='fasp',
      version='1.1',
      packages=['fasp',
                'fasp.runner',
                'fasp.search',
                'fasp.loc',
                'fasp.workflow'],
      include_package_data=True,
      install_requires=install_requires
      )