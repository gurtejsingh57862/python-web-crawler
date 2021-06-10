from pymongo import MongoClient
from datetime import datetime, timedelta
import string, random, os, requests
from bs4 import BeautifulSoup
from config import mongodb_URL

def connectToDatabase():
    client = MongoClient(mongodb_URL)  # Establish a connection to MongoDB
    db = client["scraper"]                            # create a database object referencing a new database, called “scraper”
    collection = db["Links"]                           # create collection, called "Links"
    return collection

def saveToDatabase(url, collection, source_Link):
    try:
        res = requests.get(url, timeout=10)
        if not documentInDatabase(res.url, collection):
            soup = BeautifulSoup(res.content, 'html5lib')
            random_file = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
            with open('htmlFiles/{}.html'.format(random_file), 'w', encoding="utf-8") as file:
                file.write(soup.prettify())
            file_path = ((os.path.dirname(__file__)) + '\htmlFiles\{}.html'.format(random_file)) 
            link = {
                'Link': res.url,
                'Source_Link': source_Link,
                'Is_Crawled': False,
                'Last_Crawl_Dt': '',
                'Response_Status': res.status_code,
                'Content_type': res.headers['Content-Type'],
                'Content_length': res.headers['Content-Length'] if "Content-Length" in res.headers else '',
                'File_path': file_path,
                'Created_at': datetime.now()
            }
            collection.insert_one(link)
            print(res.url)
    except Exception as error:
        print(error)
        pass

def documentCount(collection):
    return collection.count_documents({})

def documentInDatabase(url, collection):
    data = collection.find({ "Link": url})
    for d in data:
        return True
    return False

def getPendingLinks(collection):
    links = collection.find({"$or": [{"Is_Crawled": False},{"Last_Crawl_Dt":{ "$lt": datetime.now() - timedelta(days=1)}}]})
    return links

def updateDocument(document, collection):
    collection.update_one({ "_id": document["_id"]}, { "$set": {
        'Is_Crawled': True,
        'Last_Crawl_Dt': datetime.now()
    }})