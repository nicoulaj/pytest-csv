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

from ._builtin import *
from ._ids import *

BUILTIN_COLUMNS_REGISTRY = {
    ID: IdColumn(),
    MODULE: ModuleColumn(),
    NAME: NameColumn(),
    FILE: FileColumn(),
    DOC: DocColumn(),
    STATUS: StatusColumn(),
    DURATION: DurationColumn(),
    MESSAGE: MessageColumn(),
    MARKERS: MarkersColumn(with_args=False),
    MARKERS_WITH_ARGS: MarkersColumn(with_args=True),
    HOST: HostColumn(),
    USER: UserColumn(),
    SYSTEM: SystemColumn(),
    SYSTEM_RELEASE: SystemReleaseColumn(),
    SYSTEM_VERSION: SystemVersionColumn(),
    PYTHON_IMPLEMENTATION: PythonImplementationColumn(),
    PYTHON_VERSION: PythonVersionColumn(),
    WORKING_DIRECTORY: WorkingDirectoryColumn()
}
