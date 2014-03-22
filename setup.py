#!/usr/bin/env python

import os
import sys

import usergrid

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'usergrid'
]

requires = []

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()

setup(
    name='usergrid',
    version=usergrid.__version__,
    description='Python Usergrid SDK',
    long_description=readme + '\n\n' + history,
    author='Alan Boudreault',
    author_email='boudreault.alan@gmail.com',
#    url='',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'usergrid': 'usergrid'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'
    ),
)
