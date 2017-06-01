Documentation
============

Local documentation
--------------------

We are using Sphinx to create the (this) documentation.

The Documentation will be served under http://localhost:15672 as soon as :doc:`docker` is started.

The files for creation are under ``docs/``, the config file for `Sphinx <http://sphinx-doc.org/>`_ is called ``conf.py``

If needed, you can manually update it with::

    fab doc                # Builds the documentation once
    fab doc:autobuild      # Starts the sphinx-autobuild server


Swagger
--------------------

Swagger is used to print an API documentation, accessible within http://localhost:8000/api/docs.

You need to be signed in to access all endpoints.
