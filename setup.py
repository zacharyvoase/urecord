#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup
import os.path as p

VERSION = open(p.join(p.dirname(p.abspath(__file__)), 'VERSION')).read().strip()

setup(
    name='urecord',
    version=VERSION,
    description='A structured record metaclass.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/urecord',
    package_dir={'': 'src'},
    py_modules=['urecord'],
    test_suite='urecord._get_tests',
)
