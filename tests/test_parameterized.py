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


def test_with_parameters_01(testdir):
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

    result.assert_outcomes(passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, '.*test_with_parameters_01.py::test_01\[1-foo\]'),
            (MODULE, r'.*test_with_parameters_01'),
            (NAME, 'test_01\[1-foo\]'),
            (FILE, r'.*test_with_parameters_01.py'),
            (DOC, ''),
            (MARKERS, 'parametrize'),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, '.*test_with_parameters_01.py::test_01\[4-bar\]'),
            (MODULE, r'.*test_with_parameters_01'),
            (NAME, 'test_01\[4-bar\]'),
            (FILE, r'.*test_with_parameters_01.py'),
            (DOC, ''),
            (MARKERS, 'parametrize'),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, '.*test_with_parameters_01.py::test_01\[5-baz\]'),
            (MODULE, r'.*test_with_parameters_01'),
            (NAME, 'test_01\[5-baz\]'),
            (FILE, r'.*test_with_parameters_01.py'),
            (DOC, ''),
            (MARKERS, 'parametrize'),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ]
    )
