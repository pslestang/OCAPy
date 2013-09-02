#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='OCAPy',
    version='0.1.0',
    description='Python Boilerplate contains all the boilerplate you need to create a Python package.")? Python implementation of an OVH client to use with their restful API',
    long_description=readme + '\n\n' + history,
    author='Pierre-Samuel Le Stang',
    author_email='ps@lestang.fr',
    url='https://github.com/pslestang/OCAPy',
    packages=[
        'OCAPy',
    ],
    package_dir={'OCAPy': 'OCAPy'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='OCAPy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)