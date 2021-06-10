from database import connectToDatabase, documentCount, getPendingLinks, saveToDatabase
from crawler import crawl
import concurrent.futures
from config import root_URL

if __name__ == '__main__':
    collection = connectToDatabase()
    saveToDatabase(root_URL, collection, "")

    while True:
        if documentCount(collection) >=5000:
            print("Maximum limit Reached")
            break

        documents = getPendingLinks(collection)
        all_crawled = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            try:
                for document in documents:
                    all_crawled = False
                    futures.append(executor.submit(crawl, document, collection))
                for future in concurrent.futures.as_completed(futures):
                    future.result()
            except Exception as error:
                print(error)
                break
        if all_crawled:
            print("All links are crawled!")
            break


# Connect to Mongo database

# Crawl the root url

    # Make request and get response

    # Extract a href links from response

    # Process (Cleaning / forming absolute URLs / removing ) the links

    # Save links in database

# Do forever

    # Get all uncrawled links from database

    # Crawl each link separately