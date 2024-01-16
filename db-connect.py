import pymongo


def connect_to_database():
    # Connection URL
    url = "mongodb://localhost:27017/"

    # Create a MongoClient object
    client = pymongo.MongoClient(url)

    # Access a database
    db = client["mydatabase"]

    # Access a collection
    collection = db["mycollection"]

    # Perform database operations

    # Close the connection
    client.close()


# Usage in position.py
connect_to_database()
