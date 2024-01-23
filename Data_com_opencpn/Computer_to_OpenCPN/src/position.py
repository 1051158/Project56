# Import libraries

import serial
import serial.tools.list_ports
import json
import time
from pymongo import MongoClient
import certifi
from ..custom_project_lib.nmea0183_sentences import (
    NMEA0183_GEN as GEN,
)
from ..custom_project_lib.nmea0183_sentences_test import (
    NMEA0183_GEN_TEST as TEST,
)
from .dashapp import calculate_aquabot_position, get_coordinates_from_db

# lat and long in degree minutes format(DM) Between uk and ireland {Test}
# latitude = 53.679746945954754
# longitude = -5.167506462247125
latitude = 51.89832516307501
longitude = 4.418785646063367

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
    line = ser2.readline().decode("UTF-8").replace("\n", "")
    print(ser2)
    try:
        data = json.loads(line)
        print(data)
        print(data["id"])

        # tag[data["id"]].list = data["range"]
        tag = data["range"]
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
ser = serial.Serial(get_com_port(), 4800)
ser2 = serial.Serial(get_com_port(), 115200)

# Initialize the anchor and tag UWB objects
anc = []
# placebo = []
tag = []
anc_count = 4
tag_count = 1

# Define the anchor coordinates
A0X, A0Y = 0, 0
A1X, A1Y = 1000, 0
A2X, A2Y = 1000, 1340
A3X, A3Y = 0, 1340

# Start the data reading loop
ser2.write("begin".encode("UTF-8"))
ser2.reset_input_buffer()

while True:
    # print("A")
    distance_from_anchors = get_coordinates_from_db()

    # Distances from each anchor
    distance_from_A0 = int(distance_from_anchors[0][0])
    # print (distance_from_A0)
    distance_from_A1 = int(distance_from_anchors[0][1])
    distance_from_A2 = int(distance_from_anchors[0][2])

    # Calculate the Aquabot's position
    x, y = calculate_aquabot_position(
        distance_from_A0, distance_from_A1, distance_from_A2
    )
    # print(x, y)
    # Use any sentences here and send them to OpenCPN with serial.write((sentence + '\r\n').encode())

    # Create a minimal GGA sentence with only latitude and longitude
    gga = GEN.gga(
        lat=latitude + (y / 1000000),
        long=longitude + (x / 1000000),
        fix_quality=1,
        satellites=10,
        horizontal_dilution_of_precision=0.1,
        elevation_above_sea_level=255.747,
        elevation_unit="M",
        geoid=-32.00,
        geoid_unit="M",
        age_of_correction_data_seconds="01",
        correction_station_id="0000",
    )

    # gga = TEST.test_gga(
    #     latitude=latitude + y, longitude=longitude + x, print_sentence=True
    # )
    # Send the NMEA sentence to the serial port
    ser.write(
        (gga + "\r\n").encode()
    )  # Ensure to add line ending (\r\n) for NMEA sentences
    # read_data()
    read_data()
