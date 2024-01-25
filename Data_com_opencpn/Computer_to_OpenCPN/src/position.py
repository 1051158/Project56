# Import libraries

import serial
import serial.tools.list_ports
import json
from pymongo import MongoClient
import certifi
from ..custom_project_lib.nmea0183_sentences import (
    NMEA0183_GEN as GEN,
)
from ..custom_project_lib.socket_connection import (
    SOCKET_CONNECTION as SC,
)
from scipy.optimize import minimize
import numpy as np
from multiprocessing import shared_memory
import struct

# Shared memory setup
shared_memory_name = "coords_shm"
coords_size = 8 * 2  # 2 floats (8 bytes each for double precision)

# Create shared memory array
shm = shared_memory.SharedMemory(name=shared_memory_name, create=True, size=coords_size)

# lat and long in degree minutes format(DM) Between uk and ireland {Test}
# latitude = 53.679746945954754
# longitude = -5.167506462247125
latitude, longitude = 51.91735281648919, 4.483809124878688

# Define color constants
RED = [255, 0, 0]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

uri = "mongodb+srv://aleniriskic:lr9iu3bI3WtRXLJa@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client.RangeData

# name the trip, change "trip1" to whatever you want
collection = db.trip1

anchor_coordinates = [
    {"xA0": 0, "yA0": 0},
    {"xA1": 350, "yA1": 0},
    {"xA2": 350, "yA2": 350},
    {"xA3": 0, "yA3": 350},
]


# Function to calculate the Aquabot's position using the three-point algorithm
def calculate_tag_position(
    distance_to_anchor1, distance_to_anchor2, distance_to_anchor3, distance_to_anchor4
):
    """
    Calculate the position of the tag using trilateration with four anchors.
    :param distance_to_anchor1: Distance from the tag to Anchor 1.
    :param distance_to_anchor2: Distance from the tag to Anchor 2.
    :param distance_to_anchor3: Distance from the tag to Anchor 3.
    :param distance_to_anchor4: Distance from the tag to Anchor 4.
    :return: (x, y) position of the tag.
    """
    # Define fixed anchor positions
    anchor_positions = [
        (anchor_coordinates[0]["xA0"], anchor_coordinates[0]["yA0"]),
        (anchor_coordinates[1]["xA1"], anchor_coordinates[1]["yA1"]),
        (anchor_coordinates[2]["xA2"], anchor_coordinates[2]["yA2"]),
        (anchor_coordinates[3]["xA3"], anchor_coordinates[3]["yA3"]),
    ]

    # Distances from tag to each anchor
    distances = [
        distance_to_anchor1,
        distance_to_anchor2,
        distance_to_anchor3,
        distance_to_anchor4,
    ]

    # Objective function to minimize
    def objective_function(point):
        x, y = point
        return sum(
            (np.sqrt((x - ax) ** 2 + (y - ay) ** 2) - d) ** 2
            for (ax, ay), d in zip(anchor_positions, distances)
        )

    # Initial guess: Use centroid of anchors
    initial_guess = np.mean(anchor_positions, axis=0)

    # Minimize the objective function
    result = minimize(objective_function, initial_guess, method="Nelder-Mead")

    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed")


def get_com_port():
    """
    Returns the COM port selected by the user.
    """
    print(
        "--------------------------------------------------------------------------------"
    )
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
    print(
        "--------------------------------------------------------------------------------"
    )
    return ports[port_index].device


def read_data(x, y):  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    Reads the data from the serial port, updates the UWB objects, and uploads the data to MongoDB.
    """
    # print(f"Serial: {ser}")z
    try:
        # print(f"Data: {data}")
        # print(f"Data identification: {data['id']}")

        # tag[data["id"]].list = data["range"]
        # tag = data["range"
        # remove data["range"] and data["id"] from data
        data.pop("range")
        data.pop("id")

        # Insert data into MongoDB
        collection.insert_one(data)

    except ValueError:
        print("[LOG]" + line)


# Set up the serial port !!!!!!!!!!!!!!!!!!!!
ser = serial.Serial(get_com_port(), 115200)

# Initialize the anchor and tag UWB objects
anc = []
tag = []
anc_count = 4
tag_count = 1

# Start the data reading loop !!!!!!!!!!!!!!!!
ser.write("begin".encode("UTF-8"))
ser.reset_input_buffer()

sc = SC()  # socket_connection object
sc.tcp()  # TCP connection to OpenCPN, can also be udp()
try:  # Handle KeyboardInterrupt
    while True:
        line = ser.readline().decode("UTF-8").replace("\n", "")
        data = json.loads(line)
        # print(data["range"])

        distance_from_A0 = data["range"][0]
        distance_from_A1 = data["range"][1]
        distance_from_A2 = data["range"][2]
        distance_from_A3 = data["range"][3]

        # Calculate the Aquabot's position
        x, y = calculate_tag_position(
            distance_from_A0, distance_from_A1, distance_from_A2, distance_from_A3
        )

        struct.pack_into("dd", shm.buf, 0, x, y)  # 'dd' for two doubles

        # Use any sentences here and send them to OpenCPN

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

        hdt = GEN.hdt(heading_degrees_true=45.0, true="T")

        sc.change_data(gga)
        sc.send_data()

        sc.change_data(hdt)
        sc.send_data()

        read_data(x, y)

except KeyboardInterrupt:
    print(
        "--------------------------------------------------------------------------------"
    )
    print("| [~~~/---] Program is terminated by the user!")
    sc.close()
    exit()

# Compile with: python3 -m Data_com_opencpn.Computer_to_OpenCPN.src.position
