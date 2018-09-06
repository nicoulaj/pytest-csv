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

from collections import OrderedDict

import csv
import re
import six
from distutils.version import LooseVersion
from pytest import __version__ as pytest_version
from tabulate import tabulate

__TAB_ARGS__ = dict(tablefmt='grid', headers='keys', showindex='always')


def assert_outcomes(result, passed=0, skipped=0, failed=0, error=0, xpassed=0, xfailed=0):
    if LooseVersion(pytest_version) < LooseVersion('3.8'):
        result.assert_outcomes(passed=passed,
                               skipped=skipped,
                               failed=failed,
                               error=error)
    else:
        result.assert_outcomes(passed=passed,
                               skipped=skipped,
                               failed=failed,
                               error=error,
                               xpassed=xpassed,
                               xfailed=xfailed)


def assert_csv_equal(actual_csv_path, *expected_csv_rows):
    with open(actual_csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        actual = [OrderedDict(sorted(row.items(), key=lambda item: reader.fieldnames.index(item[0]))) for row in reader]

    expected = [OrderedDict(row) for row in expected_csv_rows]

    if len(expected) != len(actual):
        raise AssertionError('Expected %i rows in CSV file, got %i' % (len(expected), len(actual)))

    for i, (expected_row, actual_row) in enumerate(zip(expected, actual)):

        expected_row_keys, actual_row_keys = set(six.iterkeys(expected_row)), set(six.iterkeys(actual_row))
        if expected_row_keys != actual_row_keys:
            raise AssertionError('CSV has a different set of columns from expected (columns %s)' %
                                 ','.join(expected_row_keys.symmetric_difference(actual_row_keys)))

        for (expected_name, expected_value), (actual_name, actual_value) in zip(six.iteritems(expected_row),
                                                                                six.iteritems(actual_row)):

            if expected_name != actual_name:
                raise AssertionError('CSV file has different column order from expected '
                                     '(at row %i, expected column "%s", got column "%s").'
                                     '\n\nExpected:\n%s'
                                     '\n\nActual:\n%s' % (i,
                                                          expected_name,
                                                          actual_name,
                                                          tabulate(expected, **__TAB_ARGS__),
                                                          tabulate(actual, **__TAB_ARGS__)))

            if not re.match(r'^%s$' % expected_value, actual_value, re.DOTALL):
                raise AssertionError('CSV file is different from expected '
                                     '(at row %i, column "%s").'
                                     '\n\nExpected:\n%s'
                                     '\n\nActual:\n%s' % (i,
                                                          actual_name,
                                                          tabulate(expected, **__TAB_ARGS__),
                                                          tabulate(actual, **__TAB_ARGS__)))
