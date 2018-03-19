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

from pytest_csv import *
from ._utils import assert_csv_equal


def test_custom_columns_01(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name,status')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_custom_columns_01'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
    ])


def test_custom_columns_02(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module', 'name', 'status')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_custom_columns_02'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
    ])


def test_custom_columns_03(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'module,name', 'status')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_custom_columns_03'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
    ])


def test_custom_columns_04(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', ' module  , name', ' status')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (MODULE, r'.*test_custom_columns_04'),
        (NAME, 'test_01'),
        (STATUS, PASSED),
    ])
