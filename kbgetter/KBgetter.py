import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.request import urlretrieve
from tinydb import TinyDB
from os import walk, mkdir, path as Path
import re
import time
from bs4 import BeautifulSoup

"""Module giggles
"""

class FSGetter(object):
    """The base class used to get information from the specified instance of FreshService Solutions area.

:param username: User name for login to FreshService API(2.0).
:type username: str, required.
:param password: Password for login to Freshservice API(2.0). *When using an API key the password will be "X"*.
:type password: str, required.
:param kb_url: The URL for the instance of the FreshService API.
:type kb_url: str, required.
:param kb_path: The path to the local folder where the knowledgebase will be created. If not set this varialbe will need to be set and make_directories called to create the directory structure for the local knowledgebase.
:type kb_path: str, optional (default = '').
:param  kb_name: The name of the folder to be created where the local knowledgebase will be created.
:type kb_name: str, optional (default = 'KB').
"""
    def __init__(self, username, password, kb_url, kb_path='',kb_name='KB'):
        """Construtor method. Sets the class variables and creates the local file structure for the knowledgebase.
"""
        self.username = username
        self.password = password
        self.kb_url = kb_url
        self.kb_path = kb_path
        self.kb_name = kb_name
        #if kb_folder then create the base folder structure
        if kb_path:
            self.make_directories()
            
    #base functions
    def make_directories(self):
        """Creates the local file struture for the knowledgebase. Sets the local paths for where the files will be stored.
"""
        try:
            #create base folder and subfolders
            self.path = Path.join(self.kb_path, self.kb_name)
            dir_exists = Path.exists(self.path)
            if not dir_exists:
                mkdir(self.path)
            #create articles, holds the articles from fresh service and uses their image sources and links
            self.apath = Path.join(self.path,'articles')
            dir_exists = Path.exists(self.apath)
            if not dir_exists:
                mkdir(self.apath)
            #create localarticles, hold the local articles using local img src and links
            #this will be used for intial build and cleanup build
            self.lapath = Path.join(self.path,'localarticles')
            dir_exists = Path.exists(self.lapath)
            if not dir_exists:
                mkdir(self.lapath)
            #create images, holds the images for the articles
            self.ipath = Path.join(self.path,'images')
            dir_exists = Path.exists(self.ipath)
            if not dir_exists:
                mkdir(self.ipath)                
        except Exception as e:
            print(e, e.args)

    def build_kb(self):
         """Create the database and build and populate the categories, folders, and folder_articles tables.

:return: A list of the dicts for categories and folders, and the count of folder_articles.
:rtype: list
"""
         #create the DB and populate categoris and folders
         db = TinyDB('db.json')
         #get categories and folders then insert into db
         categories = self.get_categories(db)
         folders = self.get_folders(categories, db)
         #get folder articles and write to database
         folder_articles = self.get_folder_articles(folders, db)
         db.close()
         print("%s folder_articles completed"%folder_articles)
         return [categories, folders, folder_articles]
    
    def get_categories(self, db):
        """Creates the categories table, retrieves the categories from FreshService, and populates the categories table in the database.

:param db: The TinyDB database created for the knowledgebase.
:type db: TinyDB instance, required.
:return: Categories contained in the insntance of FreshService Solutions.
:rtype: dict
"""
        print("Do Categories")
        table_categories = db.table('categories')
        response = requests.get("%s/api/v2/solutions/categories"%self.kb_url,
                            auth = HTTPBasicAuth(self.username, self.password))
        categories = json.loads(response.text)
        categories = categories['categories']
        table_categories.insert_multiple(categories)
        print("Categories completed")
        return categories

    def get_folders(self, categories, db):
        """Creates the folders table, retrieves the folders from FreshService, and populates the folders table in the database.

:param categories: The categories from the specified instance of FreshService Solutions.
:type categories: dict, required.
:param db: The TinyDB database created for the knowledgebase.
:type db: TinyDB instance, required.
:return: Folders contained in the insntance of FreshService Solutions.
:rtype: dict
"""
        #do request get folders for categories
        print("Do folders")
        table_folders = db.table('folders')
        rfolders = []
        for category in categories:
            response = requests.get("%s/api/v2/solutions/folders?category_id=%s"%(self.kb_url,category['id']),
                                    auth = HTTPBasicAuth(self.username, self.password))
            folders = json.loads(response.text)
            rfolders.extend(folders['folders'])
            print("\t%s-%s"%(folders['folders'][0]['id'],folders['folders'][0]['name']))
        table_folders.insert_multiple(rfolders)
        print("Folders completed")
        return rfolders

    def get_folder_articles(self, folders, db):
        """Creates the folder_articles table, retrieves the articles from each folder from FreshService, and populates the folder_articles table in the database. The articles retrieved from FreshService folders are contained in a single json file, converted into a dict, then stored in the local database.

:param folders: The folders from the specified instance of FreshService Solutions.
:type folders: dict, required.
:param db: The TinyDB database created for the knowledgebase.
:type db: TinyDB instance, required.
:return: The count of folder articles inserted into the folder_articles table.
:rtype: int
"""
        print("Do folder articles")
        articles_table = db.table('folder_articles')
        fcount = 0
        for folder in folders:
            response = requests.get("%s/api/v2/solutions/articles?folder_id=%s"%(self.kb_url,folder['id']),
                                    auth = HTTPBasicAuth(self.username, self.password))
            articles = json.loads(response.text)
            articles = articles['articles']
            articles_table.insert_multiple(articles)
            fcount += 1
            print('\t%s-%s'%(folder['id'],folder['name']))
        print('Folders completed')
        return fcount
            
    def article_to_html(self, article, folders, categories):
        """Create html for articles retrieved from the database, remove invalid characters, and clean them using BeautifulSoup

:param article: The article from the folder_articles table.
:type article: str, required
:param folders: The folder where the article is stored in FreshService.
:type folders: list, required
:param categories: The category where the folder for the article is stored in FreshService.
:type categories: list, required
:return: html for the article
:rtype: str
"""
        data = article['description']
        modified = article['updated_at']
        modified = modified.replace("T"," @ ")
        title = article['title']
        category = categories[article['category_id']]
        folder = folders[article['folder_id']]                    
        thtml = re.sub(r'(?<=font-family:)(.*?)(?=;)',' Arial, sans-serif',data)
        html = '''<!DOCTYPE html>
<html>
<head>
<title>%s</title>
</head>
<body>
<h1>%s</h1>
<p><b>Group: %s - %s</b></p>
<p><i>Modified on: %s</i></p>
%s
</body>
</html>'''%(title,title,category,folder,modified,thtml)
        
        html = html.replace('\u202f'," ")
        html = html.replace('\"' , '"')
        html = html.replace("\'" , "'")
        html = html.replace("\n","")
        html = html.replace('\xa0' , ' ')
        soup = BeautifulSoup(html,'html.parser')
        html = soup.prettify()
        return html
    
    def make_articles(self, current_categories=[]):
        """Get individual articles from the database based on the provided categories, pass them to article_to_html, and write the html code to the local articles folder.

:param current_categories: The list of category IDs from which the local html articles will be created. The articles created will retain all information from FreshService including href and img src locations. If no list is passed the function will retrieve articles from all categories. If a list of categories is provided only articles from the categories provided will be created.
:type current_categories: list, optional (if blank retrieve articles from all categories).
:return: The total number of articles created.
:rtype: int
"""
        db = TinyDB('db.json')
        db_folder_articles = db.table('folder_articles')
        dbfolders = db.table('folders')
        dbcategories = db.table('categories')
        #get folder information for insertion into document
        folders = {}
        for f in dbfolders:
            folders[f['id']] = f['name']
        #get category information for insertion into document
        categories = {}
        for c in dbcategories:
            categories[c['id']] = c['name']
        if not current_categories:
            current_categories = categories
        #get articles and write to file in articles if in current categories
        fcount = 0
        for article in db_folder_articles:
            if article['category_id'] in current_categories:
                html = self.article_to_html(article,folders,categories)
                article_path = Path.join(self.apath,'%s.html'%article['id'])
                f = open(article_path,'w')
                f.write(html)
                f.close()
                fcount += 1
        db.close()
        return fcount

    def make_local_articles(self):
        """Create articles for the local knowledgebase from the articles folder and download the article images. This replaces all the FreshService hrefs and img srcs with a relative path to the local files.

:return: The total number of articles created.
:rtype: int
"""
        print("Do local articles")
        fn = []
        for (dirpath, dirnames, filenames) in walk(self.apath):
            fn.extend(filenames)
        fcount = 0
        for name in fn:
            a_id = name.split('.')[0]
            article_path = Path.join(self.apath,name)
            print(article_path)
            f = open(article_path,'r')
            z = f.read()
            f.close()
            a = re.findall(r'(?<=src=")(.*?)(?=")',z)
            img_src=[]
            x = 1
            #get images, save, change img src to local
            for url in a:
                if url[0:4].lower() == "http":
                    image_path = Path.join(self.ipath,'%s-%s.png'%(a_id,x))
                    urlretrieve(url,image_path)
                    z = z.replace(url,'../images/%s-%s.png'%(a_id,x))
                    x +=1
                    time.sleep(.1)
            #change hrefs to local
            a = re.findall(r'(?<=a href=")(.*?)(?=")',z)
            for url in a:
                url_article_id = re.findall(r"\D(\d{11})\D"," "+url+" ")
                if url_article_id:
                    z = z.replace(url,'./%s.html'%url_article_id[0])
            local_article_path = Path.join(self.lapath,name)
            f = open(local_article_path,'w')
            f.write(z)
            f.close()
            fcount += 1
            if fcount % 25 == 0:
                print("\t%s"%fcount)
                time.sleep(1)
        print('Local articles completed')
        return fcount

if __name__ == '__main__':
    pass

   








    
