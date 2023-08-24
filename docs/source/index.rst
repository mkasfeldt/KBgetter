.. FSGetter documentation master file, created by
   sphinx-quickstart on Mon Nov 29 14:57:54 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FSGetter's documentation!
====================================
FSGetter is a python package used to pull FreshService knowledge base articles to a local machine.

Installation Requirements
--------------------------
* Python 3.7+
* pip 21.3.1+

pip Installation
-----------------

.. code-block::

	pip install kbgetter

>>> from KBgetter import FSGetter
>>> kb = KBGetter('my_api_key','X','https://mycompany.freshservice.com','./')
>>> builder = kb.build_kb()
>>> make_articles = kb.make_articles(current_categories)
>>> print('%s articles created'%make_articles)
>>> make_local = kb.make_local_articles()
>>> print('%s local articles created'%make_local)


User Guide
-------------------------------------
.. toctree::
   :maxdepth: 3
   
   intro
   examples
   API
   links

Useful Links
-------------
* `kbgetter on PyPi <https://pypi.org/project/kbgetter/>`_.
* `kbgetter on GitHub <https://github.com/mkasfeldt/KBgetter>`_.
* `FreshService API Reference <https://api.freshservice.com/>`_.
* `Find your FreshService API key <https://api.freshservice.com/#authentication>`_.



