Django Extensions Too
=====================

Author:Tim Santor tsantor@xstudios.agency

Overview
========

Django Extensions is a collection of custom extensions for the Django
Framework.

Features
========

-  TODO

Installation
============

To install Django Extensions Too, simply:

::

    pip install django-extensions-too

To install the development version:

::

    pip install git+https://bitbucket.org/tsantor/django-extensions-too.git@<tag>

Documentation
=============

Documentation is available at TODO

Issues
======

If you experience any issues, please create an
`issue <https://bitbucket.org/tsantor/django-extensions-too/issues>`__
on Bitbucket.


History
=======

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

0.1.0 (2017-03-30)
------------------

-  First release on PyPI.

0.1.1 (2017-04-03)
------------------

-  Fixed a bug with an outdated permissions method call in
   ``fix_proxy_permissions`` command.

0.1.2 (2017-04-03)
------------------

-  Added a ``delete_unreferenced_files`` command which deletes all files
   in MEDIA\_ROOT that are not referenced in the database.


