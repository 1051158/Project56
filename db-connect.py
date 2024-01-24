from pymongo.mongo_client import MongoClient
import certifi


def connect_to_mongodb(uri):
    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile=certifi.where())

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


uri = "mongodb+srv://aleniriskic:lr9iu3bI3WtRXLJa@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
connect_to_mongodb(uri)
