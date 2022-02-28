# apps



## Makefile

This project uses a Makefile for various tasks. Some of the available tasks
are listed below.

* `make clean` - Clean build artifacts out of your project
* `make test` - Run Unit Tests (using nose)
* `make sdist` - Build a Python source distribution
* `make rpm` - Build an RPM
* `make docs` - Build the Sphinx documentation
* `make lint` - Get a pep8 compliance report about your code
* `make artifacts` - Build an RPM and the Python source distribution.
* `make` - Equivalent to `make test lint docs artifacts`

## src/apps/orp_apps_proj/local_settings.py

Please include any local development settings in this file. Do not check this
into code review. It is included in the .gitignore file by default, so it will
not appear in any source code control commands.

## The etc folder

The `etc` or "editiable text configuration" directory contains files which
configure how this application runs in production.  

### etc/opt/orp/orp_apps_proj/orp_apps_proj_settings.py

This file will override settings in production. Be sure to define the
"ALLOWED_HOSTS" using the hostnames that your site will be hosted at, otherwise
the system will refuse all requests. This is a good place to improve your
production logging configuration, as well.

### etc/httpd/conf.d/orp_apps_proj.conf

This file is used to set up apache to serve this project. Use this if you would
like to change the context that the project is hosted add, change the production
pythonpath, or tune WSGI for more efficient service.
