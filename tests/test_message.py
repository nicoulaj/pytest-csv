# ----------------------------------------------------------------------
# pytest-csv - https://github.com/nicoulaj/pytest-csv
# copyright (c) 2018-2019 pytest-csv contributors
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


def test_skipped_with_message(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.skip('this test is broken')
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, skipped=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_skipped_with_message.py::test_01'),
        (MODULE, r'.*test_skipped_with_message'),
        (NAME, 'test_01'),
        (FILE, r'.*test_skipped_with_message.py'),
        (DOC, ''),
        (MARKERS, 'skip'),
        (STATUS, SKIPPED),
        (MESSAGE, '.*this test is broken.*'),
        (DURATION, r'.*'),
    ])


def test_xfail_with_message(testdir):
    testdir.makepyfile('''
        import pytest

        @pytest.mark.xfail(reason='this test is expected to fail')
        def test_01():
            raise Exception()
    ''')

    result = testdir.runpytest('--csv', 'tests.csv')

    assert_outcomes(result, xfailed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_xfail_with_message.py::test_01'),
        (MODULE, r'.*test_xfail_with_message'),
        (NAME, 'test_01'),
        (FILE, r'.*test_xfail_with_message.py'),
        (DOC, ''),
        (MARKERS, 'xfail'),
        (STATUS, XFAILED),
        (MESSAGE, r'.*this test is expected to fail.*'),
        (DURATION, r'.*'),
    ])
