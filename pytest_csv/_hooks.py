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


def pytest_csv_register_columns(columns):
    """
    Called on plugin initialization.

    Use it to add your own column types (or override the builtin ones).

    For instance, in conftest.py:
    >>>         from pytest_csv import Column
    >>>
    >>>         class MyColumn(Column):
    >>>             def run(self, report):
    >>>                 yield 'my column', 'my value'
    >>>
    >>>         def pytest_csv_register_columns(columns):
    >>>             columns['my_column'] = MyColumn()

    Then run pytest with your new column:

        $ py.test --csv tests.csv --csv-columns id,status,my_column

    :param columns: dictionary of (column id, CSVColumn object)
    """
