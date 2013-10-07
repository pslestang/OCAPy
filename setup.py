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

readme = open('README.md').read()

setup(
    name='OCAPy',
    version='0.2.1',
    description='Python client implementing OVH RESTful API',
    long_description=readme,
    author='Pierre-Samuel Le Stang',
    author_email='ps@lestang.fr',
    url='https://github.com/pslestang/OCAPy',
    packages=[
        'OCAPy',
    ],
    package_dir={'OCAPy': 'OCAPy'},
    include_package_data=True,
    install_requires=[
        'requests>=1.0.0',
    ],
    license="GPLv3",
    zip_safe=False,
    keywords='OCAPy',
    classifiers=[
        'Development Status :: 2 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7.5',
    ],
    test_suite='tests',
)
