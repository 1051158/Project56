from flask import Flask
from pymongo import MongoClient
import certifi

app = Flask(__name__)


@app.route("/")
def list_ranges():
    uri = "mongodb+srv://aleniriskic:0hZpyfFParfakoMe@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client.RangeData

    collection = db["trip1"]
    entries = collection.find()

    # Extracting the 'range' field from each entry and converting it to a string
    ranges = [str(entry["range"]) for entry in entries]

    return "<br>".join(ranges)


if __name__ == "__main__":
    app.run(debug=True)
