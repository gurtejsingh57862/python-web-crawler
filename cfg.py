# File to store info about all variables related to application configuration

"""

client            :  MongoDB connection client
db                :  Database object referencing a new database, called “scraper”
collection        :  Collection object of collection “Links”

url               :  Initial url i.e. "https://flinkhub.com/"
res and response  :  Response from requests get command
inlink            :  List from database for find command to check a link to be present or not
link_in_database  :  A boolean variable for specifying inlink values
soup              :  Response from a beautiful command
random_file       :  A random string name generated
file_path         :  Path to the html file created
link              :  Document for a link details
scrape_it         :  A function for scraping a link
check_post        :  A bollean variable to check from where exception has raised in nested try except block
new_url           :  Complete url after combining relative url and url url from where it is generated
temp_url          :  Storing response url temporarily
temp_index        :  Temporary index for domain extention check
find_index        :  Function to calculate the temp_index

all_crawled       :  A boolean variable for checking whether all links are crawled or not in a database
data              :  Contain list of documents that are required to be crawled

"""