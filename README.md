Vittles
=======

Vittles is a [Django](http://www.djangoproject.com/) web application for
entering and viewing recipes. It is still in the early experimental phases, but
has basic functionality for entering foods, units, ingredients, recipes, and
nutritional information through the Django admin interface, as well as for
viewing recipes in an easy-to-read format.

Additional documentation is on [ReadTheDocs](http://vittles.rtfd.org).

Setup
-----

You'll probably want to set up a virtual environment for Vittles using
[virtualenv](http://pypi.python.org/pypi/virtualenv) or
[virtualenvwrapper](http://pypi.python.org/pypi/virtualenvwrapper). Refer to
those projects' docs for instructions.

Once you have a virtual environment activated, install Vittles' dependencies:

    $ cd /path/to/vittles
    $ pip install < reqs.txt

Edit `settings.py` and define where you want the database to live:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME: '/some/path/vittles.sqlite3',
        }
    }

Save, then sync:

    $ ./manage.py syncdb

This will load some basic data from `core/fixtures/initial_data.yaml` to get
you started, including a bunch of foods, units, and equivalences.

Start the development webserver:

    $ ./manage.py runserver

Then visit http://127.0.0.1:8000/admin to start entering recipes, and
http://127.0.0.1:8000/cookbook to view the recipes you've entered.


Copyright
---------

The MIT License

Copyright (c) 2010 Eric Pierce

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

