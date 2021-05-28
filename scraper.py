import requests, string, random, os, time
from bs4 import BeautifulSoup
from  datetime import datetime, timedelta
from db.db import collection
import concurrent.futures

def find_index(temp_url):
    if ".com" in temp_url:
        return temp_url.find(".com")+5
    elif ".co" in temp_url:
        return temp_url.find(".co")+4
    elif ".org" in temp_url:
        return temp_url.find(".org")+5
    elif ".us" in temp_url:
        return temp_url.find(".us")+4
    elif ".net" in temp_url:
        return temp_url.find(".net")+5
    elif ".blog" in temp_url:
        return temp_url.find(".blog")+6
    elif ".io" in temp_url:
        return temp_url.find(".io")+4
    elif ".biz" in temp_url:
        return temp_url.find(".biz")+5
        
url = "https://flinkhub.com/"

try:
    res = requests.get(url, timeout=10)
    inlink = collection.find({ "Link": res.url})
    link_in_database = False
    for z in inlink:
        link_in_database = True
    if not link_in_database:
        soup = BeautifulSoup(res.content, 'html5lib')
        random_file = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
        with open('htmlFiles/{}.html'.format(random_file), 'w', encoding="utf-8") as file:
            file.write(soup.prettify())
        file_path = ((os.path.dirname(__file__)) + '\htmlFiles\{}.html'.format(random_file)) 
        link = {
            'Link': res.url,
            'Source Link': '',
            'Is Crawled': False,
            'Last Crawl Dt': '',
            'Response Status': res.status_code,
            'Content type': res.headers['Content-Type'],
            'Content length': res.headers['Content-Length'] if "Content-Length" in res.headers else '',
            'File path': file_path,
            'Created at': datetime.now()
        }
        collection.insert_one(link)
except Exception as error:
    print(error)

def scrape_it(x, timeout = 10):
    collection.update_one({ "_id": x["_id"]}, { "$set": {
        'Is Crawled': True,
        'Last Crawl Dt': datetime.now()
    }})
    res = requests.get(x["Link"], timeout=timeout)
    soup = BeautifulSoup(res.content, 'html5lib')
    for y in soup.find_all('a', href = True):
        if collection.count_documents({}) >= 5000:
            raise Exception("Maximum limit reached")
        
        check_post = False
        if (y.get('href') != ' '):
            try:
                response = requests.get(y.get('href'), timeout=timeout)
                check_post = True
                inlink = collection.find({ "Link": response.url})
                link_in_database = False
                for z in inlink:
                    link_in_database = True
                if not link_in_database:
                    soup = BeautifulSoup(response.content, 'html5lib')
                    random_file = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
                    with open('htmlFiles/{}.html'.format(random_file), 'w', encoding="utf-8") as file:
                        file.write(soup.prettify())
                    file_path = ((os.path.dirname(__file__)) + '\htmlFiles\{}.html'.format(random_file))

                    link = {
                        'Link': response.url,
                        'Source Link': res.url,
                        'Is Crawled': False,
                        'Last Crawl Dt': '',
                        'Response Status': response.status_code,
                        'Content type': response.headers['Content-Type'],
                        'Content length': response.headers['Content-Length'] if "Content-Length" in response.headers else '',
                        'File path': file_path,
                        'Created at': datetime.now()
                    }
                    collection.insert_one(link)
                    print(response.url)
            except Exception as error:
                if not check_post:
                    newurl = ""
                    if (len(y.get('href')) and y.get('href')[0] == "/"):
                        temp_url = res.url
                        temp_index = find_index(temp_url)
                        newurl = temp_url.replace(temp_url[temp_index:],"") + y.get('href').replace("/","")
                        try:
                            response = requests.get(newurl, timeout=timeout)
                            inlink = collection.find({ "Link": response.url})
                            link_in_database = False
                            for z in inlink:
                                link_in_database = True
                            if not link_in_database:
                                soup = BeautifulSoup(response.content, 'html5lib')
                                random_file = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
                                with open('htmlFiles/{}.html'.format(random_file), 'w', encoding="utf-8") as file:
                                    file.write(soup.prettify())
                                file_path = ((os.path.dirname(__file__)) + '\htmlFiles\{}.html'.format(random_file)) 

                                link = {
                                    'Link': response.url,
                                    'Source Link': res.url,
                                    'Is Crawled': False,
                                    'Last Crawl Dt': '',
                                    'Response Status': response.status_code,
                                    'Content type': response.headers['Content-Type'],
                                    'Content length': response.headers['Content-Length'] if "Content-Length" in response.headers else '',
                                    'File path': file_path,
                                    'Created at': datetime.now()
                                }
                                collection.insert_one(link)
                                print(response.url)
                        except Exception as error:
                            print(2, error)
                else:
                    print(1, error)
    time.sleep(5)

while True:
    if collection.count_documents({}) >= 5000:
        print("Maximum limit reached")
        break
    all_crawled = True
    data = collection.find({"$or": [{"Is Crawled": False},{"Last Crawl Dt":{ "$lt": datetime.now() - timedelta(days=1)}}]})
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        try:
            for x in data:
                all_crawled = False
                futures.append(executor.submit(scrape_it, x=x))
            for future in concurrent.futures.as_completed(futures):
                future.result()
        except Exception as error:
            print(error)

    if all_crawled:
        print("All links crawled")
        break