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

import platform
import sys

import pytest

from pytest_csv.column import *
from ._utils import assert_csv_equal


def test_column_host(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name,status,host')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_column_host'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
        (HOST, platform.node()),
    ])


@pytest.mark.skipif(sys.platform == 'win32', reason='get_user() is not reliable on windows')
def test_column_user(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name,status,user')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_column_user'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
        (USER, get_user()),
    ])


def test_column_system(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name,status,system')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_column_system'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
        (SYSTEM, platform.system()),
    ])


def test_column_python_implementation(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name,status,python_implementation')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_column_python_implementation'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
        (PYTHON_IMPLEMENTATION, platform.python_implementation()),
    ])


def test_column_python_version(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name,status,python_version')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_column_python_version'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
        (PYTHON_VERSION, platform.python_version()),
    ])
