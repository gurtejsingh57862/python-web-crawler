from pprint import pprint
# Importing MongoClient from 
from pymongo import MongoClient

# Establish a connection to MongoDB
client = MongoClient('mongodb://localhost:27017')

# create a database object referencing a new database, called “scraper”
db  = client["scraper"]

# create collection, called "Links"
collection = db["Links"]
