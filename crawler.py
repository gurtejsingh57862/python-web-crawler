from database import documentCount, saveToDatabase, updateDocument
import requests
from bs4 import BeautifulSoup
from database import saveToDatabase

def crawl(document, collection):
    updateDocument(document, collection)
    response = getResponse(document["Link"], 10)
    links = getValidLinks(response)
    for link in links:
        if documentCount(collection) >=5000:
            raise Exception("Maximum Limit Reached")
        saveToDatabase(link, collection, document["Link"])

def getResponse(url, timeout):
    return requests.get(url, timeout=timeout)

def getValidLinks(response):
    links = []
    soup = BeautifulSoup(response.content, 'html5lib')
    href = soup.find_all('a', href = True)

    for href in href:
        if href.get('href').startswith("#") or href.get('href').startswith("tel:") or href.get('href').startswith("javascript:;") or href.get('href').startswith(" "):
            continue

        if href.get('href').startswith("https://") or href.get('href').startswith("http://"):
            links.append(href.get('href'))
            continue

        if href.get('href').startswith("/"):
            temp_url = response.url
            temp_index = find_index(temp_url)
            newurl = temp_url.replace(temp_url[temp_index:],"") + href.get('href').replace("/","")
            links.append(newurl)
    
    return links

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