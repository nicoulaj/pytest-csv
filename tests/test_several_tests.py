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


def test_several_tests(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
            
        def test_02():
            pass
            
        def test_03():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    result.assert_outcomes(passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, '.*test_several_tests.py::test_01'),
            (MODULE, r'.*test_several_tests'),
            (NAME, 'test_01'),
            (FILE, r'.*test_several_tests.py'),
            (DOC, ''),
            (MARKERS, ''),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, '.*test_several_tests.py::test_02'),
            (MODULE, r'.*test_several_tests'),
            (NAME, 'test_02'),
            (FILE, r'.*test_several_tests.py'),
            (DOC, ''),
            (MARKERS, ''),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, '.*test_several_tests.py::test_03'),
            (MODULE, r'.*test_several_tests'),
            (NAME, 'test_03'),
            (FILE, r'.*test_several_tests.py'),
            (DOC, ''),
            (MARKERS, ''),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ]
    )
