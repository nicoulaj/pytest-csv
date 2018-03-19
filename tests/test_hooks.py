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


def test_register_custom_column(testdir):
    testdir.makeconftest("""
        import pytest
        from pytest_csv import Column

        class MyColumn(Column):
            def run(self, report):
                yield 'my column', 'my value'

        def pytest_csv_register_columns(columns):
            columns['my_column'] = MyColumn()
        """)

    testdir.makepyfile('''
        def test_01():
            pass
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,my_column')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_register_custom_column.py::test_01'),
        ('my column', 'my value'),
    ])
