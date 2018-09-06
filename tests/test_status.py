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


def test_passed(testdir):
    testdir.makepyfile('''
        def test_01():
            assert True
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_passed.py::test_01'),
        (MODULE, r'.*test_passed'),
        (NAME, 'test_01'),
        (FILE, r'.*test_passed.py'),
        (DOC, ''),
        (MARKERS, ''),
        (STATUS, PASSED),
        (MESSAGE, ''),
        (DURATION, r'.*'),
    ])


def test_failed(testdir):
    testdir.makepyfile('''
        def test_01():
            assert False
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, failed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_failed.py::test_01'),
        (MODULE, r'.*test_failed'),
        (NAME, 'test_01'),
        (FILE, r'.*test_failed.py'),
        (DOC, ''),
        (MARKERS, ''),
        (STATUS, FAILED),
        (MESSAGE, '.+'),
        (DURATION, r'.*'),
    ])


def test_error(testdir):
    testdir.makepyfile('''
        import pytest
    
        @pytest.fixture
        def some_fixture():
            raise Exception('this fixture is broken')
    
        def test_01(some_fixture):
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, error=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_error.py::test_01'),
        (MODULE, r'.*test_error'),
        (NAME, 'test_01'),
        (FILE, r'.*test_error.py'),
        (DOC, ''),
        (MARKERS, ''),
        (STATUS, ERROR),
        (MESSAGE, r'.*this fixture is broken.*'),
        (DURATION, r'.*'),
    ])


def test_skipped(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.skip
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, skipped=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_skipped.py::test_01'),
        (MODULE, r'.*test_skipped'),
        (NAME, 'test_01'),
        (FILE, r'.*test_skipped.py'),
        (DOC, ''),
        (MARKERS, 'skip'),
        (STATUS, SKIPPED),
        (MESSAGE, '.*'),
        (DURATION, r'.*'),
    ])


def test_skipped_whole_module(testdir):
    testdir.makepyfile('''
        import pytest

        pytestmark = pytest.mark.skip

        def test_01():
            pass
            
        def test_02():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, skipped=2)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, '.*test_skipped_whole_module.py::test_01'),
            (MODULE, r'.*test_skipped_whole_module'),
            (NAME, 'test_01'),
            (FILE, r'.*test_skipped_whole_module.py'),
            (DOC, ''),
            (MARKERS, 'skip'),
            (STATUS, SKIPPED),
            (MESSAGE, '.*'),
            (DURATION, r'.*'),
        ],
        [
            (ID, '.*test_skipped_whole_module.py::test_02'),
            (MODULE, r'.*test_skipped_whole_module'),
            (NAME, 'test_02'),
            (FILE, r'.*test_skipped_whole_module.py'),
            (DOC, ''),
            (MARKERS, 'skip'),
            (STATUS, SKIPPED),
            (MESSAGE, '.*'),
            (DURATION, r'.*'),
        ]
    )


def test_xfail(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.xfail
        def test_01():
            raise Exception()
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, xfailed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_xfail.py::test_01'),
        (MODULE, r'.*test_xfail'),
        (NAME, 'test_01'),
        (FILE, r'.*test_xfail.py'),
        (DOC, ''),
        (MARKERS, 'xfail'),
        (STATUS, XFAILED),
        (MESSAGE, '.*'),
        (DURATION, r'.*'),
    ])


def test_xpassed(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.xfail
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, xpassed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_xpassed.py::test_01'),
        (MODULE, r'.*test_xpassed'),
        (NAME, 'test_01'),
        (FILE, r'.*test_xpassed.py'),
        (DOC, ''),
        (MARKERS, 'xfail'),
        (STATUS, XPASSED),
        (MESSAGE, ''),
        (DURATION, r'.*'),
    ])
