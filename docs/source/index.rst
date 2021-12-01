.. FSGetter documentation master file, created by
   sphinx-quickstart on Mon Nov 29 14:57:54 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FSGetter's documentation!
====================================
FSGetter is used to pull FreshService knowledgebase articles to a local machine.

>>> from KBgetter import FSGetter
>>> kb = KBGetter('my_api_key','X','https://mycompany.freshservice.com','./')
>>> builder = kb.build_kb()
>>> make_articles = kb.make_articles(current_categories)
>>> print('%s articles created'%make_articles)
>>> make_local = kb.make_local_articles()
>>> print('%s local articles created'%make_local)

-------------------------------------
Introduction
-------------------------------------
.. toctree::
   :maxdepth: 2
   
   intro
   examples

-------------------------------------
API Reference
-------------------------------------
.. toctree::
   :maxdepth: 2
   
   KBgetter
   