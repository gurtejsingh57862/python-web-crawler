# File to store info about all variables related to application configuration

"""
main.py        :  Contain main funcytion
database.py    :  Contain function related to database operations
crawler.py     :  Contain function related to scraping and link validations

"""

root_URL = "https://flinkhub.com/"

mongodbAtlas_password = ""
mongodb_URL = 'mongodb+srv://taskapp:' + mongodbAtlas_password + '@cluster0.anp6t.mongodb.net/Crawler?retryWrites=true&w=majority'