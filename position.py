# Import libraries

import serial
import serial.tools.list_ports
import json
import time
from pymongo import MongoClient
import certifi


# Define color constants
RED = [255, 0, 0]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

uri = "mongodb+srv://aleniriskic:0hZpyfFParfakoMe@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client.RangeData

# name the trip, change "trip1" to whatever you want
collection = db.trip1


def get_com_port():
    """
    Returns the COM port selected by the user.
    """
    ports = serial.tools.list_ports.comports()
    if len(ports) == 0:
        print("No COM ports available")
        return None

    print("Available COM Ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")

    port_index = -1
    while port_index < 0 or port_index >= len(ports):
        try:
            port_index = int(input("Select COM port number: "))
        except ValueError:
            print("Please enter a valid number")

    return ports[port_index].device


def read_data():
    """
    Reads the data from the serial port, updates the UWB objects, and uploads the data to MongoDB.
    """
    line = ser.readline().decode("UTF-8").replace("\n", "")

    try:
        data = json.loads(line)
        print(data)
        print(data["id"])

        tag[data["id"]].list = data["range"]
        tag[data["id"]].cal()

        # Add anchor coordinates to data
        data["anchor_coordinates"] = [
            {"x": A0X, "y": A0Y},
            {"x": A1X, "y": A1Y},
            {"x": A2X, "y": A2Y},
            {"x": A3X, "y": A3Y},
        ]

        # Insert data into MongoDB
        collection.insert_one(data)

    except ValueError:
        print("[LOG]" + line)


# Set up the serial port
ser = serial.Serial(get_com_port(), 115200)

# Initialize the anchor and tag UWB objects
anc = []
tag = []
anc_count = 4
tag_count = 1

# Define the anchor coordinates
A0X, A0Y = 0, 0
A1X, A1Y = 400, 0
A2X, A2Y = 400, 400
A3X, A3Y = 0, 400

# Start the data reading loop
ser.write("begin".encode("UTF-8"))
ser.reset_input_buffer()

while True:
    read_data()
