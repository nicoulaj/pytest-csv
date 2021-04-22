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


def test_with_custom_markers(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01
        @pytest.mark.my_marker_02
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, passed=1)

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


def test_with_custom_markers_with_args(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=45,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,markers_with_args')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_custom_markers_with_args.py::test_01'),
        (MARKERS, 'my_marker_01\(foobar\),my_marker_02\(a=45,b=test\),my_marker_03\(21,foo,a=32,b=test\)'),
    ])


def test_with_custom_markers_as_columns(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=32,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,markers_as_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_custom_markers_as_columns.py::test_01'),
        ('my_marker_01', 'foobar'),
        ('my_marker_02', 'a=32,b=test'),
        ('my_marker_03', '21,foo,a=32,b=test'),
    ])


def test_with_custom_markers_args_as_columns(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=32,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,markers_args_as_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_custom_markers_args_as_columns.py::test_01'),
        ('my_marker_01.0', 'foobar'),
        ('my_marker_02.a', '32'),
        ('my_marker_02.b', 'test'),
        ('my_marker_03.0', '21'),
        ('my_marker_03.1', 'foo'),
        ('my_marker_03.a', '32'),
        ('my_marker_03.b', 'test'),
    ])
