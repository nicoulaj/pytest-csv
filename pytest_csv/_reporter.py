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

import csv
import os

import pytest
import six
from _pytest.mark import MarkInfo


class CSVReporter(object):
    def __init__(self,
                 csv_path,
                 columns,
                 delimiter,
                 quote_char):
        self._csv_path = csv_path
        self._columns = columns
        self._delimiter = delimiter
        self._quote_char = quote_char
        self._rows = []

    @pytest.mark.hookwrapper
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        report.test_doc = item.obj.__doc__ or ''
        report.test_args = item.callspec.params if hasattr(item, 'callspec') else {}
        report.test_markers = [v for v in six.itervalues(item.keywords) if isinstance(v, MarkInfo)]

    def pytest_runtest_logreport(self, report):
        if report.when != 'call' and report.passed:
            return
        self._rows.append({column: dict(column(report)) if callable(column) else {key: str(column)}
                           for key, column in six.iteritems(self._columns)})

    def pytest_sessionfinish(self, session):
        if not self._rows or hasattr(session.config, 'slaveinput'):
            return

        directory = os.path.dirname(self._csv_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        headers = {column: list(sorted(set(header
                                           for row in self._rows
                                           for header in six.iterkeys(row[column]))))
                   for column in six.itervalues(self._columns)}

        with open(self._csv_path, 'w') as out:
            writer = csv.writer(out, delimiter=self._delimiter, quotechar=self._quote_char, quoting=csv.QUOTE_MINIMAL)

            writer.writerow([header
                             for column in six.itervalues(self._columns)
                             for header in headers[column]])

            for row in self._rows:
                writer.writerow([row[column].get(header, '')
                                 for column in six.itervalues(self._columns)
                                 for header in headers[column]])

        session.config.hook.pytest_csv_written(csv_path=self._csv_path)

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'CSV report: %s' % self._csv_path)
