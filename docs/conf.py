# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('extensions'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage',
              'sphinx.ext.viewcode', 'sphinx.ext.intersphinx',
              'sphinx.ext.todo', 'sphinx.ext.extlinks']

todo_include_todos = True
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []
add_function_parentheses = True
#add_module_names = True
# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

project = u'KBgetter'
copyright = u'2021, Matt Kasfeldt'

version = ''
release = ''

sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes']
html_theme = 'sphinx_rtd_theme'

todo_include_todos = True