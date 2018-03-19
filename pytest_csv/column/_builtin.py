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

import getpass
import os
import platform

from _pytest.runner import TestReport

from ._api import Column, ConstantColumn
from ._ids import *
from ._status import *
from ._utils import parse_node_id, format_mark_info


class IdColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        yield ID, report.nodeid


class ModuleColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        mod, cls, func, params = parse_node_id(report.nodeid)
        yield MODULE, mod or ''


class ClassColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        mod, cls, func, params = parse_node_id(report.nodeid)
        yield CLASS, cls or ''


class FunctionColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        mod, cls, func, params = parse_node_id(report.nodeid)
        yield FUNCTION, func or ''


class ParamsColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        mod, cls, func, params = parse_node_id(report.nodeid)
        yield PARAMS, params or ''


class NameColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        mod, cls, func, params = parse_node_id(report.nodeid)
        yield NAME, '%s[%s]' % (func, params) if params else func


class FileColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        yield FILE, report.location[0]


class DocColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        yield DOC, getattr(report, 'test_doc', '').strip()


class StatusColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        if report.passed:
            yield STATUS, XPASSED if hasattr(report, 'wasxfail') else PASSED
        elif report.failed:
            yield STATUS, XFAILED if hasattr(report, 'wasxfail') else ERROR if report.when != 'call' else FAILED
        elif report.skipped:
            yield STATUS, XFAILED if hasattr(report, 'wasxfail') else SKIPPED


class MessageColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        if report.passed:
            if hasattr(report, 'wasxfail'):
                yield MESSAGE, report.wasxfail
            else:
                yield MESSAGE, ''

        elif report.failed:
            if hasattr(report, 'wasxfail'):
                yield MESSAGE, report.wasxfail
            else:
                if hasattr(report.longrepr, 'reprcrash'):
                    yield MESSAGE, report.longrepr.reprcrash.message
                elif isinstance(report.longrepr, (unicode, str)):
                    yield MESSAGE, report.longrepr
                else:
                    yield MESSAGE, str(report.longrepr)

        elif report.skipped:
            if hasattr(report, 'wasxfail'):
                yield MESSAGE, report.wasxfail
            else:
                _, _, message = report.longrepr
                yield MESSAGE, message


class DurationColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        yield DURATION, str(getattr(report, 'duration', ''))


class MarkersColumn(Column):
    def __init__(self, with_args):
        self.with_args = with_args

    def run(self, report):
        # type: (TestReport) -> str
        yield MARKERS, ','.join(format_mark_info(mark, self.with_args) for mark in getattr(report, 'test_markers', []))


class HostColumn(ConstantColumn):
    def __init__(self):
        super(HostColumn, self).__init__(HOST, platform.node())


class UserColumn(ConstantColumn):
    def __init__(self):
        super(UserColumn, self).__init__(USER, getpass.getuser())


class SystemColumn(ConstantColumn):
    def __init__(self):
        super(SystemColumn, self).__init__(SYSTEM, platform.system())


class SystemReleaseColumn(ConstantColumn):
    def __init__(self):
        super(SystemReleaseColumn, self).__init__(SYSTEM_RELEASE, platform.release())


class SystemVersionColumn(ConstantColumn):
    def __init__(self):
        super(SystemVersionColumn, self).__init__(SYSTEM_VERSION, platform.version())


class PythonImplementationColumn(ConstantColumn):
    def __init__(self):
        super(PythonImplementationColumn, self).__init__(PYTHON_IMPLEMENTATION, platform.python_implementation())


class PythonVersionColumn(ConstantColumn):
    def __init__(self):
        super(PythonVersionColumn, self).__init__(PYTHON_VERSION, platform.python_version())


class WorkingDirectoryColumn(Column):
    def run(self, report):
        # type: (TestReport) -> str
        yield WORKING_DIRECTORY, os.getcwd()
