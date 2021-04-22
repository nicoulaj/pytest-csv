#!/usr/bin/env python
# ----------------------------------------------------------------------
# pytest-csv - https://github.com/nicoulaj/pytest-csv
# copyright (c) 2018-2021 pytest-csv contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------


import os
from setuptools import setup, find_packages

from pytest_csv import __prog__, __version__, __author__, __email__, __description__, __keywords__, __license__, __url__

setup(
    name=__prog__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license=__license__,
    url=__url__,
    keywords=__keywords__,
    classifiers=[
        'Framework :: Pytest',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'pytest>=6.0',
        'six>=1.0.0'
    ],
    extras_require={
        'test': [
            'pytest-xdist>=1.29.0',
            'pytest-flake8>=1.0.7',
            'tabulate>=0.8.2'
        ]
    },
    entry_points={
        'pytest11': [
            'pytest_csv = pytest_csv._plugin',
        ]
    },
)
