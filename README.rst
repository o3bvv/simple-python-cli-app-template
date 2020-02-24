simple-python-cli-app-template
==============================

This is a cookiecutter_ template for generating simple Python
command-line interface (CLI) applications and utilities.

The primary audience is data science and data processing teams, however,
the template is generic enough to find a good fit in other places.

Please, refer to the project's article_ to get more info.


.. raw:: html

   <h2>Contents</h2>

.. contents::
    :local:
    :depth: 3
    :backlinks: none


Features
--------

The template provides essentials for creating, packaging, and managing
CLI applications. Among them:

* Config and params passing, overriding and validating:

  * Define and validate config structure in ``jsonschema`` format.
  * Define config defaults.
  * Optionally read configs from JSON or YAML files.
  * Optionally override config values using args defined via
    ``argparse`` or ``click``.
  * Optionally override config values using env vars.

* Logging setup:

  * Support of microsecond resolution.
  * Support of UTC or local time zone in log records.
  * Log records format.
  * Optionally inject hostname into log records.
  * Optionally format log records as JSON.

* Definition of an installable package with executable commands.
* Linting support via ``flake8``.
* Optional testing via ``pytest``.
* Helpful ``make`` commands.


Prerequisites
-------------

As this is a ``cookiecutter``'s template, make sure it's installed:

.. code-block:: bash

   pip install cookiecutter


Template invocation
-------------------

Default usage is the same as for any other ``cookiecutter`` templates:
call ``cookiecutter`` and pass template's URL as a param:


.. code-block:: bash

   cookiecutter https://github.com/oblalex/simple-python-cli-app-template


or a GitHub repo name via ``gh`` shortcut:

.. code-block:: bash

   cookiecutter gh:oblalex/simple-python-cli-app-template


Next, follow ``cookiecutter``'s questions to set up params and get a minimal
working application. Refer to the following section to see which params are
available.

..

  **NOTE**: Please, refer to ``cookiecutter``'s documentation regarding
  ``.cookiecutterrc`` file and ``--no-input`` argument in case
  user-prompt is unwelcome.


Params
------

The template accepts several parameters to configure a project being created.
Parameters have default values. The full set of template's params is listed
below.


``project_name``
  Name of a project (``string``).
  Used in documentation. Defaults of several other params are calculated
  from it.

  Default value: ``"Simple Python CLI App"``.


``package_name``
  Name of Python package to create (``string``).

  Default value is calculated from ``project_name`` via slugification.

  Example value: ``"simple_python_cli_app"``.


``executable_name``
  Name of an executable file to create during package installation
  (``string``).

  Default value is calculated from ``project_name`` via slugification.

  Example value: ``"simple-python-cli-app"``.


``class_name_prefix``
  Prefix used for package class names (``string``).

  Default value is calculated from ``project_name`` via slugification.

  Example value: ``"SimplePythonCliApp"``.


``env_var_name_prefix``
  Prefix used for names of env vars (``string``).
  Used to override config values.

  Default value is calculated from ``project_name`` via slugification.

  Example value: ``"SIMPLE_PYTHON_CLI_APP"``.


``project_short_description``
  Short description of the package being created (``string``).
  Used in documentation.

  Default value: ``"Simple Python CLI application"``.


``project_url``
  Project's URL (``string``).

  Default value: ``""`` (empty string).


``version``
  Project's version (``string``).

  Default value: ``"1.0.0"``.


``author_name``
  Name of package's author or owning team (``string``).

  Default value: ``"John Doe"``.


``author_email``
  Email of package's author or owning team (``string``).

  Default value: ``"john.doe@example.com"``.


``author_username``
  Username of package's author or owning team (``string``).

  Default value: ``"john.doe"``.


``create_author_file``
  Whether to create or not ``AUTHORS.rst`` file (``boolean``).

  Default value: ``y``.


``command_line_interface``
  Command-line parser to use (``integer`` as a choice number of ``string``'s).

  Choices:

  #. ``argparse``
  #. ``click``

  Default value: ``1``.


``config_file_format``
  Config file format to use (``integer`` as a choice number of ``string``'s).

  Choices:

  #. ``YAML``
  #. ``JSON``
  #. ``no config file``

  Default value: ``1``.


``logging_time_zone``
  Time zone to use in timestamps of log records
  (``integer`` as a choice number of ``string``'s).

  Choices:

  #. ``utc``
  #. ``local``

  Default value: ``1``.


``logging_include_hostname``
  Whether to include hostname into log records or not (``boolean``).

  Default value: ``y``.


``logging_format_json``
  Whether to format log records as json or not (``boolean``).

  Default value: ``n``.


``use_pytest``
  Whether to use ``pytest`` as test runner or not (``boolean``).

  Default value: ``n``.


MAKE commands
-------------

This template includes a ``Makefile`` with commands useful to perform
common duty tasks:

``clean``
  Remove all build, test, coverage and Python artifacts.


``clean-build``
  Remove build artifacts.


``clean-pyc``
  Remove Python file artifacts.


``clean-test``
  Remove test and coverage artifacts.


``lint``
  Check style with ``flake8``.


``test``
  Run tests quickly with the default Python.


``dist``
  Builds source and ``wheel`` package.


``install``
  Install the package to the active Python's site-packages.


``install-e``
  Install the package into the active Python's site-packages
  in editable mode via ``pip``.


``dev-deps``
  Install development dependencies via ``pip``.


``test-deps``
  Install testing dependencies via ``pip``.


Caveats
-------

As ``cookiecutter`` uses ``Jinja2`` as a template engine and as certain
functionality provided by this template is optional, resulting files may
contain extra newlines or be missing them.


..

.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _article: https://medium.com/@oblalex/python-template-for-data-processing-apps-2674aa05d1d7
