#
#
# DON"T USE
#
#

import serial
import pynmea2
import random
import time
import math

# Replace 'COMX' with the appropriate virtual COM port on your system
serial_port = 'COM20'  # For Windows

# Open the serial port
try:
    ser = serial.Serial(serial_port, 4800, timeout=1)
    print(f"Connected to {serial_port}")
except serial.SerialException as e:
    print(f"Failed to connect to {serial_port}: {e}")
    exit()

# Function to generate random initial movement
def initial_movement():
    # Generate a random direction (in degrees)
    initial_direction = random.uniform(0, 360)
    return initial_direction

# Function to calculate new coordinates based on the initial direction
def calculate_new_coordinates(latitude, longitude, direction, distance):
    # Convert the direction from degrees to radians
    direction_rad = direction * (3.14159 / 180.0)

    # Calculate new coordinates based on initial position, direction, and distance (assuming a small movement)
    new_latitude = latitude + (distance * 0.00001 * 60 * (180 / 3.14159)) * math.cos(direction_rad)
    new_longitude = longitude + (distance * 0.00001 * 60 * (180 / 3.14159)) * math.sin(direction_rad)
    return new_latitude, new_longitude

# Initial latitude and longitude in degrees and decimal minutes format
latitude = 6324.1241  # Example latitude in DM.MMMM format
longitude = 1844.0367  # Example longitude in DM.MMMM format

# Initial direction and distance for movement
direction = initial_movement()
distance = 10  # Simulated movement distance in meters (adjust as needed)

while True:
    # Calculate new coordinates based on the initial direction
    latitude, longitude = calculate_new_coordinates(latitude, longitude, direction, distance)

    # Create a minimal GGA sentence with only latitude and longitude
    gga = pynmea2.GGA('GP', 'GGA', (
        time.strftime("%H%M%S"),
        "{:.4f}".format(latitude),
        'N',
        "{:.4f}".format(longitude),
        'W',
        '1',  # Fix quality (1 = GPS fix)
        '10',  # Number of satellites
        '0.9',  # Horizontal dilution of precision
    ))

    # Get the NMEA sentence in string format
    nmea_sentence = gga.render()

    # Send the NMEA sentence to the serial port
    ser.write((nmea_sentence + '\r\n').encode())  # Ensure to add line ending (\r\n) for NMEA sentences

    # Print the generated NMEA sentence (optional)
    # print(f"Generated NMEA sentence: {nmea_sentence}")

    # Wait for a few seconds before sending the next update
    time.sleep(0.5)  # Adjust the time interval as needed
