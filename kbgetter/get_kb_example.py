from KBgetter import FSGetter

#Please get your API key by following the instructions at https://api.freshservice.com/#authentication
#username must be the API key. username/password is no longer supported
api_key = 'fg8TVzifZhv5B7KIRHHF'
#password will always be 'X' for API key usernames
password = 'X'
#kb_url is the base instance of FreshService for an organization
kb_url = 'https://convergint.freshservice.com'
#kb_name, in this example, is the directory where this script and KBgetter.py is stored and is a relative path
kb_name = './'
#current_categories is passed to make_articles to limit the articles created by category
#the categories listed here are the categories that have D365 and associated systems documentation
current_categories = [17000047310, 17000046518, 17000046519, 17000046523, 17000046520, 17000046521, 17000046522, 17000048074]

kb = FSGetter(api_key,password,kb_url,'./')
builder = kb.build_kb()
#passing current_categories to make_articles limits the articles created by category.
#if nothing is passed to make_articles all articles in solutions will be created.
make_articles = kb.make_articles(current_categories)
print('%s articles created'%make_articles)
make_local = kb.make_local_articles()
print('%s local articles created'%make_local)
