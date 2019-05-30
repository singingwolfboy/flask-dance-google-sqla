Automated Tests
===============

To run the tests, you need to install the test dependencies
specified in the ``test-requirements.txt`` file.
You can install them with ``pip``, like this:

.. code-block:: bash

    pip install -r test-requirements.txt

Then you can run the tests using the ``pytest`` command:

.. code-block:: bash

    pytest

Fixtures
--------

The ``conftest.py`` file contains the `Pytest fixtures`_ that
the tests use. We want to use the ``db_session``
fixture provided by `pytest-flask-sqlalchemy
<https://github.com/jeancochrane/pytest-flask-sqlalchemy>`_,
so we define a ``_db`` fixture and set ``mocked-sessions``
in the ``pytest.ini`` file.

Cassettes
---------

The ``cassettes`` directory contains HTTP sessions recorded bt Betamax_,
which the automated tests can replay. To record new HTTP sessions,
delete the files in that directory, and then run the tests again.

When making live HTTP requests to Google, such as when you record
new HTTP sessions, you must have a valid OAuth token for Google.
Put this OAuth token in the ``GOOGLE_OAUTH_ACCESS_TOKEN`` environment
variable, and the automated tests will automatically pick it up.

.. _Pytest: https://pytest.org/
.. _Betamax: https://betamax.readthedocs.io/
.. _Pytest fixtures: https://docs.pytest.org/en/latest/fixture.html
