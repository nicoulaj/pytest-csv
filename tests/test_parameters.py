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

from pytest_csv.column import *
from ._utils import assert_csv_equal, assert_outcomes


def test_with_parameters(testdir):
    testdir.makepyfile('''
        import pytest
        @pytest.mark.parametrize("a,b", [
            (1, 'foo'),
            (4, 'bar'),
            (5, 'baz'),
        ])
        def test_01(a,b):
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_parameters.py::test_01\[1-foo\]'),
            (MODULE, r'.*test_with_parameters'),
            (NAME, r'test_01\[1-foo\]'),
            (FILE, r'.*test_with_parameters.py'),
            (DOC, ''),
            (MARKERS, 'parametrize'),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, r'.*test_with_parameters.py::test_01\[4-bar\]'),
            (MODULE, r'.*test_with_parameters'),
            (NAME, r'test_01\[4-bar\]'),
            (FILE, r'.*test_with_parameters.py'),
            (DOC, ''),
            (MARKERS, 'parametrize'),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, r'.*test_with_parameters.py::test_01\[5-baz\]'),
            (MODULE, r'.*test_with_parameters'),
            (NAME, r'test_01\[5-baz\]'),
            (FILE, r'.*test_with_parameters.py'),
            (DOC, ''),
            (MARKERS, 'parametrize'),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ]
    )


def test_with_parameters_column(testdir):
    testdir.makepyfile('''
        import pytest
        @pytest.mark.parametrize("a,b", [
            (1, 'foo'),
            (4, 'bar'),
            (5, 'baz'),
        ])
        def test_01(a,b):
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,parameters')

    assert_outcomes(result, passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_parameters_column.py::test_01\[1-foo\]'),
            (PARAMETERS, 'a=1,b=foo'),
        ],
        [
            (ID, r'.*test_with_parameters_column.py::test_01\[4-bar\]'),
            (PARAMETERS, 'a=4,b=bar'),
        ],
        [
            (ID, r'.*test_with_parameters_column.py::test_01\[5-baz\]'),
            (PARAMETERS, 'a=5,b=baz'),
        ]
    )


def test_with_parameters_as_columns(testdir):
    testdir.makepyfile('''
        import pytest
        @pytest.mark.parametrize("a,b", [
            (1, 'foo'),
            (4, 'bar'),
            (5, 'baz'),
        ])
        def test_01(a,b):
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,parameters_as_columns')

    assert_outcomes(result, passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_parameters_as_columns.py::test_01\[1-foo\]'),
            ('a', '1'),
            ('b', 'foo'),
        ],
        [
            (ID, r'.*test_with_parameters_as_columns.py::test_01\[4-bar\]'),
            ('a', '4'),
            ('b', 'bar'),
        ],
        [
            (ID, r'.*test_with_parameters_as_columns.py::test_01\[5-baz\]'),
            ('a', '5'),
            ('b', 'baz'),
        ]
    )


def test_with_parameters_as_columns_and_fixtures(testdir):
    testdir.makepyfile('''
        import pytest
        @pytest.mark.parametrize("a,b", [
            (1, 'foo'),
            (4, 'bar'),
            (5, 'baz'),
        ])
        def test_01(request,a,b):
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,parameters_as_columns')

    assert_outcomes(result, passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_parameters_as_columns_and_fixtures.py::test_01\[1-foo\]'),
            ('a', '1'),
            ('b', 'foo'),
        ],
        [
            (ID, r'.*test_with_parameters_as_columns_and_fixtures.py::test_01\[4-bar\]'),
            ('a', '4'),
            ('b', 'bar'),
        ],
        [
            (ID, r'.*test_with_parameters_as_columns_and_fixtures.py::test_01\[5-baz\]'),
            ('a', '5'),
            ('b', 'baz'),
        ]
    )
