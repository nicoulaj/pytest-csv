pytest-csv
==========

.. image:: https://img.shields.io/pypi/v/pytest-csv.svg
   :target: https://pypi.org/project/pytest-csv
   :alt: last release

.. image:: https://img.shields.io/pypi/pyversions/pytest-csv.svg
   :target: https://pypi.org/project/pytest-csv
   :alt: pypi package

.. image:: https://img.shields.io/badge/pytest-6.0%2B-green.svg
   :target: https://pytest.org
   :alt: pytest supported versions

.. image:: https://github.com/nicoulaj/pytest-csv/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/nicoulaj/pytest-csv/actions
   :alt: continuous integration

----

**CSV output for pytest.**

----

Installation
------------

Install using pip:
::

  pip install pytest-csv

Usage
-----

* To enable the CSV report:

  ::

    py.test --csv tests.csv

* To customize the CSV delimiter/quoting characters:

  ::

    py.test --csv tests.csv --csv-delimiter ';' --csv-quote-char '"'

* To customize the columns:

  ::

    py.test --csv tests.csv --csv-columns host,function,status,duration,parameters_as_columns

* This is the reference of all available columns:

  +----------------------------+--------------------------------------------------------------------------+
  | Column                     | Description                                                              |
  +============================+==========================================================================+
  | ``id``                     | pytest test identifier                                                   |
  +----------------------------+--------------------------------------------------------------------------+
  | ``module``                 | test module name                                                         |
  +----------------------------+--------------------------------------------------------------------------+
  | ``class``                  | test class                                                               |
  +----------------------------+--------------------------------------------------------------------------+
  | ``function``               | test function name                                                       |
  +----------------------------+--------------------------------------------------------------------------+
  | ``name``                   | test name, with arguments                                                |
  +----------------------------+--------------------------------------------------------------------------+
  | ``file``                   | test module file                                                         |
  +----------------------------+--------------------------------------------------------------------------+
  | ``doc``                    | test function docstring                                                  |
  +----------------------------+--------------------------------------------------------------------------+
  | ``status``                 | test status (passed, failed, error, skipped, xpassed or xfailed)         |
  +----------------------------+--------------------------------------------------------------------------+
  | ``success``                | test status, as a boolean                                                |
  +----------------------------+--------------------------------------------------------------------------+
  | ``duration``               | test duration, in seconds                                                |
  +----------------------------+--------------------------------------------------------------------------+
  | ``duration_formatted``     | test duration, human readable                                            |
  +----------------------------+--------------------------------------------------------------------------+
  | ``message``                | error message, if any                                                    |
  +----------------------------+--------------------------------------------------------------------------+
  | ``markers``                | test markers, as a comma-separated list                                  |
  +----------------------------+--------------------------------------------------------------------------+
  | ``markers_with_args``      | test markers with their arguments, as a comma-separated list             |
  +----------------------------+--------------------------------------------------------------------------+
  | ``markers_as_columns``     | test markers, each as a separate column                                  |
  +----------------------------+--------------------------------------------------------------------------+
  | ``markers_args_as_columns``| test markers with their arguments, each as a separate column             |
  +----------------------------+--------------------------------------------------------------------------+
  | ``parameters``             | test parameters, as a comma-separated list                               |
  +----------------------------+--------------------------------------------------------------------------+
  | ``parameters_as_columns``  | test parameters, each as a separate column                               |
  +----------------------------+--------------------------------------------------------------------------+
  | ``properties``             | properties recorded using ``record_property``, as a comma-separated list |
  +----------------------------+--------------------------------------------------------------------------+
  | ``properties_as_columns``  | properties recorded using ``record_property``, each as a separate column |
  +----------------------------+--------------------------------------------------------------------------+
  | ``user``                   | current user name                                                        |
  +----------------------------+--------------------------------------------------------------------------+
  | ``host``                   | current host (from ``platform`` module)                                  |
  +----------------------------+--------------------------------------------------------------------------+
  | ``system``                 | current system name (from ``platform`` module)                           |
  +----------------------------+--------------------------------------------------------------------------+
  | ``system_release``         | current system release info (from ``platform`` module)                   |
  +----------------------------+--------------------------------------------------------------------------+
  | ``system_version``         | current system version info (from ``platform`` module)                   |
  +----------------------------+--------------------------------------------------------------------------+
  | ``python_implementation``  | current python implementation (from ``platform`` module)                 |
  +----------------------------+--------------------------------------------------------------------------+
  | ``python_version``         | current python version (from ``platform`` module)                        |
  +----------------------------+--------------------------------------------------------------------------+
  | ``working_directory``      | current working directory                                                |
  +----------------------------+--------------------------------------------------------------------------+

* To add some data directly from a test function, enable `properties_as_columns` and use:

  ::

    def test_01(record_property):
        record_property('my column 1', 42)
        record_property('my column 2', 'foo bar')

* To define new column types, in ``conftest.py`` (`more examples here <https://github.com/nicoulaj/pytest-csv/blob/master/pytest_csv/_hooks.py#L20>`_):

  ::

    def pytest_csv_register_columns(columns):
        columns['my_simple_column'] = lambda item, report: {'my column': report.nodeid}

Issues
------

Please report issues `here <https://github.com/nicoulaj/pytest-csv/issues>`_.

License
-------

This software is released under the GNU General Public License v3.0, see ``COPYING`` for details.
