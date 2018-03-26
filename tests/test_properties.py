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

from pytest_csv import *
from ._utils import assert_csv_equal

pytestmark = pytest.mark.skipif(not hasattr(junitxml, 'record_property'), reason='record_property not available')


def test_record_property(testdir):
    testdir.makepyfile('''
        def test_01(record_property):
            record_property("example_key", 1)
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,properties')

    result.assert_outcomes(passed=1)

    assert_csv_equal('tests.csv', [
        (ID, '.*test_record_property.py::test_01'),
        (PROPERTIES, 'example_key=1'),
    ])


def test_record_property_as_columns(testdir):
    testdir.makepyfile('''
        def test_01(record_property):
            pass
            
        def test_02(record_property):
            record_property("example_key", 1)
    ''')

    result = testdir.runpytest('--csv', 'tests.csv',
                               '--csv-columns', 'id,properties_as_columns')

    result.assert_outcomes(passed=2)

    assert_csv_equal(
        'tests.csv',
        [
            (ID, '.*test_record_property_as_columns.py::test_01'),
            ('example_key', '')
        ],
        [
            (ID, '.*test_record_property_as_columns.py::test_02'),
            ('example_key', '1')
        ]
    )
