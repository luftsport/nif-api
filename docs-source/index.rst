Welcome to Nif Api's documentation!
=====================================

A pythonic library to simplify the interaction to NIF soap/xml webservices. Utilizes Zeep and good intentions, returns sanitized, pythonic and snake cased data.

Example::

   from nif_api import NifApiIntegration
   username = '<app_id>/<function_id>/<app_name>'
   password = '<password>'
   integration = NifApiIntegration(username, password, realm='DST', log_file='dst.log')
   integration.get_person(<person_id>)
   >>>(True, {<person_object>})

Nif Api supports the following NIF realms:

* PROD
* DST
* DEV

.. toctree::
   :maxdepth: 1
   :caption: NIF Api

   nif_api


.. toctree::
   :maxdepth: 1
   :caption: Module index

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Recent Changes
--------------

.. git_changelog::
