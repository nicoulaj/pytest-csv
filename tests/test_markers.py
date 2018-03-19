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


def test_with_custom_markers(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01
        @pytest.mark.my_marker_02
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_custom_markers.py::test_01'),
        (MODULE, r'.*test_with_custom_markers'),
        (NAME, 'test_01'),
        (FILE, r'.*test_with_custom_markers.py'),
        (DOC, ''),
        (MARKERS, 'my_marker_01,my_marker_02'),
        (STATUS, PASSED),
        (MESSAGE, ''),
        (DURATION, r'.*'),
    ])


def test_with_custom_markers_with_value(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=32,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_custom_markers_with_value.py::test_01'),
        (MODULE, r'.*test_with_custom_markers_with_value'),
        (NAME, 'test_01'),
        (FILE, r'.*test_with_custom_markers_with_value.py'),
        (DOC, ''),
        (MARKERS, 'my_marker_01,my_marker_02,my_marker_03'),
        (STATUS, PASSED),
        (MESSAGE, ''),
        (DURATION, r'.*'),
    ])
