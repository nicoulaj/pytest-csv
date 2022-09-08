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

import csv
import os

import pytest
import six


class CSVReporter(object):
    def __init__(self,
                 csv_path,
                 columns,
                 delimiter,
                 quote_char,
                 xdist_sort):
        self._csv_path = csv_path
        self._columns = columns
        self._delimiter = delimiter
        self._quote_char = quote_char
        self._xdist_sort = xdist_sort
        self._rows = []

    @pytest.mark.hookwrapper
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()

        if report.when != 'call' and report.passed:
            return

        report._csv_rows = {column_id: dict(column(item, report)) if callable(column) else {column_id: str(column)}
                            for column_id, column in six.iteritems(self._columns)}

    def pytest_runtest_logreport(self, report):
        rows = getattr(report, '_csv_rows', None)
        if rows is not None:
            self._rows.append(rows)
        elif report.when == '???':
            # A worker crashed, and xdist called logreport with a fake report the master generated
            rows = {}
            for column_id, column in six.iteritems(self._columns):
                if callable(column):
                    try:
                        column_val = dict(column(None, report))  # The item isn't available - the master doesn't run collection
                    except Exception:
                        column_val = {}
                else:
                    column_val = {column_id: str(column)}
                rows[column_id] = column_val
            self._rows.append(rows)

    def pytest_sessionfinish(self, session):
        if not self._rows or hasattr(session.config, 'slaveinput') or hasattr(session.config, 'workerinput'):
            return

        directory = os.path.dirname(self._csv_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        headers = {column_id: list(sorted(set(header
                                              for row in self._rows
                                              for header in six.iterkeys(row[column_id]))))
                   for column_id in six.iterkeys(self._columns)}

        #find id column
        scan_id_key = 'id'

        id_index = list(headers.keys()).index(scan_id_key)  if f"'{scan_id_key}'" in str(headers.keys()) else -1

        with open(self._csv_path, 'w', newline='', encoding="utf-8") as out:
            writer = csv.writer(out, delimiter=self._delimiter, quotechar=self._quote_char, quoting=csv.QUOTE_MINIMAL)

            writer.writerow([header
                             for column_id in six.iterkeys(self._columns)
                             for header in headers[column_id]])

            if id_index == -1 or self._xdist_sort is not True:
                # if id column not founded
                for row in self._rows:
                    writer.writerow([row[column_id].get(header, '')
                                    for column_id in six.iterkeys(self._columns)
                                    for header in headers[column_id]])
            else:
                temp_lst = list()
                session_lst = list()
                for row in self._rows:
                    #move csv data to temporary list
                    temp_lst.append([row[column_id].get(header, '')
                                    for column_id in six.iterkeys(self._columns)
                                    for header in headers[column_id]])

                # extract nodeid from sessions.items classes
                for node in session.items:
                    session_lst.append(node.nodeid)

                # write the in-out-sync orders csv output
                writer.writerows(sorted(temp_lst, key = lambda i:session_lst.index(i[id_index])))

        session.config.hook.pytest_csv_written(csv_path=self._csv_path)

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'CSV report: %s' % self._csv_path)
