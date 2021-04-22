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

import pytest

from pytest_csv.column import *
from ._utils import assert_csv_equal

STANDARD_COLUMNS = set(BUILTIN_COLUMNS_REGISTRY.keys()) - {MARKERS_WITH_ARGS,
                                                           MARKERS_AS_COLUMNS,
                                                           MARKERS_ARGS_AS_COLUMNS,
                                                           PROPERTIES_AS_COLUMNS,
                                                           PARAMETERS_AS_COLUMNS}


@pytest.mark.parametrize('column', STANDARD_COLUMNS, ids=str)
def test_column(testdir, column):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', ID, column)

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [(ID, r'.*test_01'), (column, r'.*')])


def test_all_columns_enabled(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', ','.join(STANDARD_COLUMNS))

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [(name, r'.*') for name in STANDARD_COLUMNS])


@pytest.mark.parametrize('column', STANDARD_COLUMNS, ids=str)
def test_column_duplicated(testdir, column):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '--csv-columns', ID, column, column)

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [(ID, r'.*test_01'), (column, r'.*')])
