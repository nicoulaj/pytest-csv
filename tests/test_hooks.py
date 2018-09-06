# ----------------------------------------------------------------------
# pytest-csv - https://github.com/nicoulaj/pytest-csv
# copyright (c) 2018 pytest-csv contributors
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

from pytest_csv import *
from ._utils import assert_csv_equal, assert_outcomes


def test_register_custom_column_constant(testdir):
    testdir.makeconftest("""
        def pytest_csv_register_columns(columns):
            columns['my_column'] = 'foobar'
        """)

    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,my_column')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_register_custom_column_constant.py::test_01'),
        ('my_column', 'foobar'),
    ])


def test_register_custom_column_lambda(testdir):
    testdir.makeconftest("""
        def pytest_csv_register_columns(columns):
            columns['my_column'] = lambda report: {'my column': report.nodeid}
        """)

    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,my_column')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_register_custom_column_lambda.py::test_01'),
        ('my column', '.*test_register_custom_column_lambda.py::test_01'),
    ])


def test_register_custom_column_function(testdir):
    testdir.makeconftest("""

        def my_column(report):
            return {'my column': report.nodeid}

        def pytest_csv_register_columns(columns):
            columns['my_column'] = my_column
        """)

    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,my_column')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_register_custom_column_function.py::test_01'),
        ('my column', '.*test_register_custom_column_function.py::test_01'),
    ])


def test_register_custom_column_generator(testdir):
    testdir.makeconftest("""

        def my_columns(report):
            yield 'my column 1', report.nodeid
            yield 'my column 2', 42

        def pytest_csv_register_columns(columns):
            columns['my_columns'] = my_columns
        """)

    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,my_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_register_custom_column_generator.py::test_01'),
        ('my column 1', '.*test_register_custom_column_generator.py::test_01'),
        ('my column 2', '42'),
    ])


def test_csv_written(testdir):
    testdir.makeconftest("""
        import shutil

        def pytest_csv_written(csv_path):
            shutil.copy(csv_path, csv_path + '.1')
        """)

    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, passed=1)

    assert os.path.exists('tests.csv.1')
