#!/usr/bin/env python3
"""
Copyright 2018 Nick Everett
All Rights Reserved.

Licensed under the GNU General Public License v3.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

https://www.gnu.org/licenses/gpl-3.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""


import io
import os
import wifitx
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')

setup(
    name='wifitx',
    version=wifitx.__version__,
    url='https://github.com/nickever/wifi-TxRate',
    license='GNU General Public License v3.0',
    author='Nick Everett',
    author_email='njeverett@gmail.com',
    description='Command line interface for testing wifi transmission speed',
    long_description=long_description,
    keywords='wifi test speed transmission tx wifitx',
    py_modules=['wifitx'],
    entry_points={  # Optional
        'console_scripts': [
            'wifitx=wifitx:main',
        ],
    },
    platforms='macOS',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'License :: OSI Approved :: '
        'GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Networking'])