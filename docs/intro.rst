Introduction
====================================
``FSGetter`` is used to download, store, and transform solutions from FreshService using the FreshService 2.0 API. 

FreshService organizes solutions into folders. Folders are organized into categories. When downloading articles the entire folder's articles are pulled from FreshService and stored as a single record in the local database. This record is then pulled from the database and each individual article extracted and saved to  local HTML file in the article folder

Articles in the local article folder retain all information, including the links image sources to the specified FreshService instance. The articles in the the Articles folder can then be converted to use local links and image sources, and download the images for the local image sources.

The documentation for FreshService Servic Desk API 2.0 can be found `here <https://api.freshservice.com/#introduction>`_.

Installation
-------------

.. code-block::

	pip install kbgetter

Basic Usage
------------
An API key for the instance of FreshService is required to use FSGetter. The API key will be used to initialize the FSGetter class and passed as *username*. Please refer to `FreshService Autentication <https://api.freshservice.com/#authentication>`_ on how to obtain an API key.

To download, store, and transform articles from KBGetter:

1. Import FSGetter from KBgetter.

.. code-block::

	from kbgetter import FSGetter
	
2. Create an instance of FSGetter.

	* userame = Your API key
	* password = "X"
	* kb_url = The url to your instance of FreshService (ex: ``https://convergint.freshservice.com``)
	* kb_path = The local path to store the database, folders and files
	* kb_name = The name of the new folder that will created on the kb_path to house the database, folders and files

.. code-block::

	kb = KBGetter('my_api_key','X', 'https://convergint.freshservice.com','./')

3. Call the builder function to get the categories, folders and articles set from FreshService.

.. code-block::

	builder = kb.build_kb()

4. Call the make_articles function to create all the articles in the local database.

..code-block::

	make_articles = kb.make_articles()
	
5. Call make_local_articles to create the local version of the articles created in the previous step.

..code-block::

	make_local = kb.make_local_articles()
