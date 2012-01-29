.. Vittles documentation master file, created by
   sphinx-quickstart on Sun May 29 12:40:43 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Vittles
=======

Vittles is a Django_ web application for entering and viewing recipes.
Get the source code from Github_.

It is still in the early experimental phases, but has basic functionality for
entering foods, units, ingredients, recipes, and nutritional information through
the Django admin interface, as well as for viewing recipes in an easy-to-read
format.

Contents:

.. toctree::
    :maxdepth: 2

    user_manual/index
    api/index


Setup
-----

You'll probably want to set up a virtual environment for Vittles using
virtualenv_ or virtualenvwrapper_. Refer to those projects' docs for
instructions.

Once you have a virtual environment activated, install Vittles' dependencies::

    $ cd /path/to/vittles
    $ pip install -r reqs.txt

Edit `settings.py` and define where you want the database to live::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME: '/some/path/vittles.sqlite3',
        }
    }

Save, then sync::

    $ ./manage.py syncdb

This will load some basic data from `core/fixtures/initial_data.yaml` to get
you started, including a bunch of foods, units, and equivalences.

Start the development webserver::

    $ ./manage.py runserver

Then visit http://127.0.0.1:8000/admin to start entering recipes, and
http://127.0.0.1:8000/cookbook to view the recipes you've entered.

.. _Django: http://www.djangoproject.com/
.. _Github: http://github.com/wapcaplet/vittles
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://pypi.python.org/pypi/virtualenvwrapper


Developing
----------

To build the documentation::

    $ cd docs
    $ make html

To run the test suite::

    $ ./manage.py test


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

