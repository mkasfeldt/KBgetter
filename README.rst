README.rst
===========
FSGetter is used to pull FreshService knowledgebase articles to a local machine.

Documentation home: https://kbgetter.readthedocs.io/en/latest/

Examples
---------

1. Create database, articles and local articles.

.. code-block::

	from kbgetter import FSGetter

	#Please get your API key by following the instructions at https://api.freshservice.com/#authentication
	#username must be the API key. username/password is no longer supported
	api_key = 'your_api_key'
	#password will always be 'X' for API key usernames
	password = 'X'
	#kb_url is the base instance of FreshService for an organization
	kb_url = 'https://mycompany.freshservice.com'
	#kb_name, in this example, is the directory where this script and KBgetter.py is stored and is a relative path
	kb_name = './'
	#current_categories is passed to make_articles to limit the articles created by category
	#the categories' IDs (integers) listed here are the categories that have D365 and associated systems documentation
	current_categories = [523212, 523213, 523214]

	kb = FSGetter(api_key,password,kb_url,'./')
	builder = kb.build_kb()
	#passing current_categories to make_articles limits the articles created by category.
	#if nothing is passed to make_articles all articles in solutions will be created.
	make_articles = kb.make_articles(current_categories)
	print('%s articles created'%make_articles)
	make_local = kb.make_local_articles()
	print('%s local articles created'%make_local)

2. View all categories from the database.

.. code-block::

	from tinydb import TinyDB
	db = TinyDB('db.json')
	categories = db.table('categories')
	for category in categories:
		input("ID = %s, Name = %s, Description = %s"%(category['id'],category['name'],category['description']))

