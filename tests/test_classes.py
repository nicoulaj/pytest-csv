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
from ._utils import assert_csv_equal, assert_outcomes


def test_in_class(testdir):
    testdir.makepyfile('''
        class TestClass(object):
            def test_01(self):
                assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_in_class.py::TestClass::\(\)::test_01'),
        (MODULE, r'.*test_in_class'),
        (NAME, 'test_01'),
        (FILE, r'.*test_in_class.py'),
        (DOC, ''),
        (MARKERS, ''),
        (STATUS, PASSED),
        (MESSAGE, ''),
        (DURATION, r'.*'),
    ])
