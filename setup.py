# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup

import pycoda


def requirements(filename='requirements.txt'):
    with open(filename, b'r') as fh:
        return fh.read()


setup(
    name='pycoda',
    version=pycoda.__version__,
    description='Coded statement of Account (CODA) python API',
    url='https://github.com/mhemeryck/pycoda',
    install_requires=requirements(),
    author='Martijn Hemeryck',
    author_email='martijn.hemeryck@gmail.com',
    license='MIT',
    packages=['pycoda'],
    zip_safe=True,
)
