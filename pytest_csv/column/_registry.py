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
    CLASS: ClassColumn(),
    FUNCTION: FunctionColumn(),
    NAME: NameColumn(),
    FILE: FileColumn(),
    DOC: DocColumn(),
    STATUS: StatusColumn(),
    SUCCESS: SuccessColumn(),
    DURATION: DurationColumn(),
    DURATION_FORMATTED: DurationFormattedColumn(),
    MESSAGE: MessageColumn(),
    MARKERS: MarkersColumn(with_args=False),
    MARKERS_WITH_ARGS: MarkersColumn(with_args=True),
    MARKERS_AS_COLUMNS: MarkersAsColumns(),
    MARKERS_ARGS_AS_COLUMNS: MarkersArgumentsAsColumns(),
    PARAMETERS: ParametersColumn(),
    PARAMETERS_AS_COLUMNS: ParametersAsColumns(),
    PROPERTIES: PropertiesColumn(),
    PROPERTIES_AS_COLUMNS: PropertiesAsColumns(),
    HOST: HostColumn(),
    USER: UserColumn(),
    SYSTEM: SystemColumn(),
    SYSTEM_RELEASE: SystemReleaseColumn(),
    SYSTEM_VERSION: SystemVersionColumn(),
    PYTHON_IMPLEMENTATION: PythonImplementationColumn(),
    PYTHON_VERSION: PythonVersionColumn(),
    WORKING_DIRECTORY: WorkingDirectoryColumn()
}
