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

from _pytest.runner import TestReport


class Column(object):
    def run(self, report):
        # type: (TestReport) -> str
        raise NotImplementedError()

    def get_default_value(self):
        # type: () -> str
        return ''


class ConstantColumn(Column):
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def run(self, report):
        # type: (TestReport) -> str
        yield self._name, self._value
