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

import pytest
from _pytest import junitxml

from pytest_csv.column import *
from ._utils import assert_csv_equal, assert_outcomes


def test_with_xdist(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '-n', '2')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_xdist.py::test_01'),
        (MODULE, r'.*test_with_xdist'),
        (NAME, 'test_01'),
        (FILE, r'.*test_with_xdist.py'),
        (DOC, ''),
        (MARKERS, ''),
        (STATUS, PASSED),
        (MESSAGE, ''),
        (DURATION, r'.*'),
    ])


def test_with_xdist_several_tests(testdir):
    testdir.makepyfile('''
        def test_01():
            pass
            
        def test_02():
            pass
            
        def test_03():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv', '-n', '2')

    assert_outcomes(result, passed=3)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_xdist_several_tests.py::test_\d+'),
            (MODULE, r'.*test_with_xdist_several_tests'),
            (NAME, r'test_\d+'),
            (FILE, r'.*test_with_xdist_several_tests.py'),
            (DOC, ''),
            (MARKERS, ''),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, r'.*test_with_xdist_several_tests.py::test_\d+'),
            (MODULE, r'.*test_with_xdist_several_tests'),
            (NAME, r'test_\d+'),
            (FILE, r'.*test_with_xdist_several_tests.py'),
            (DOC, ''),
            (MARKERS, ''),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ],
        [
            (ID, r'.*test_with_xdist_several_tests.py::test_\d+'),
            (MODULE, r'.*test_with_xdist_several_tests'),
            (NAME, r'test_\d+'),
            (FILE, r'.*test_with_xdist_several_tests.py'),
            (DOC, ''),
            (MARKERS, ''),
            (STATUS, PASSED),
            (MESSAGE, ''),
            (DURATION, r'.*'),
        ]
    )


@pytest.mark.xfail(reason="doesn't work...")
def test_with_xdist_parametrized(testdir):
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

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,parameters_as_columns')

    assert_outcomes(result, passed=3)

    # FIXME #5: add support for order independent assert
    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_xdist_parametrized.py::test_01\[1-foo\]'),
            ('a', '1'),
            ('b', 'foo'),
        ],
        [
            (ID, r'.*test_with_xdist_parametrized.py::test_01\[4-bar\]'),
            ('a', '4'),
            ('b', 'bar'),
        ],
        [
            (ID, r'.*test_with_xdist_parametrized.py::test_01\[5-baz\]'),
            ('a', '5'),
            ('b', 'baz'),
        ]
    )


@pytest.mark.skipif(not hasattr(junitxml, 'record_property'), reason='record_property not available')
def test_with_xdist_properties(testdir):
    testdir.makepyfile('''
        def test_01(record_property):
            record_property("example_key", 1415)
    ''')

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,properties_as_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, '.*test_with_xdist_properties.py::test_01'),
            ('example_key', '1415')
        ],
    )


@pytest.mark.skipif(not hasattr(junitxml, 'record_property'), reason='record_property not available')
@pytest.mark.xfail(reason="not a pytest-csv issue, what you put in record_property must be serializable")
def test_with_xdist_properties_non_serializable(testdir):
    testdir.makepyfile('''
        def test_01(record_property):
        
            class MyClass(object):
                pass
        
            record_property("example_key", MyClass)
    ''')

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,properties_as_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, '.*test_with_xdist_properties.py::test_01'),
            ('example_key', 'MyClass')
        ],
    )


def test_with_xdist_parametrized_non_serializable_parameters(testdir):
    testdir.makepyfile('''

        class MyClass(object):
            pass

        import pytest
        @pytest.mark.parametrize("a", [MyClass])
        def test_01(a):
            assert True
    ''')

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,parameters')

    assert_outcomes(result, passed=1)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, r'.*test_with_xdist_parametrized_non_serializable_parameters.py::test_01\[MyClass\]'),
            ('parameters', 'a=<class \'test_with_xdist_parametrized_non_serializable_parameters.MyClass\'>'),
        ],
    )


@pytest.mark.xfail(reason="doesn't work...")
def test_with_xdist_custom_markers_with_args(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=45,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,markers_with_args')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, r'.*test_with_xdist_custom_markers_with_args.py::test_01'),
        (MARKERS, r'my_marker_01\(foobar\),my_marker_02\(a=45,b=test\),my_marker_03\(21,foo,a=32,b=test\)'),
    ])


@pytest.mark.xfail(reason="doesn't work...")
def test_with_xdist_custom_markers_as_columns(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=32,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,markers_as_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_xdist_custom_markers_as_columns.py::test_01'),
        ('my_marker_01', 'foobar'),
        ('my_marker_02', 'a=32,b=test'),
        ('my_marker_03', '21,foo,a=32,b=test'),
    ])


@pytest.mark.xfail(reason="doesn't work...")
def test_with_xdist_custom_markers_args_as_columns(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.my_marker_01('foobar')
        @pytest.mark.my_marker_02(a=32,b='test')
        @pytest.mark.my_marker_03(21,'foo',a=32,b='test')
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('-n', '2',
                               '--csv', 'tests.csv',
                               '--csv-columns', 'id,markers_args_as_columns')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_with_xdist_custom_markers_args_as_columns.py::test_01'),
        ('my_marker_01.0', 'foobar'),
        ('my_marker_02.a', '32'),
        ('my_marker_02.b', 'test'),
        ('my_marker_03.0', '21'),
        ('my_marker_03.1', 'foo'),
        ('my_marker_03.a', '32'),
        ('my_marker_03.b', 'test'),
    ])
