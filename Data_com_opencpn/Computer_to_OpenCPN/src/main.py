#
# USE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This script is used to send NMEA sentences to OpenCPN
# Always pair a nmea sentence with a serial.write() command
#

import serial
import socket
import time
from ..custom_project_lib.nmea0183_sentences import NMEA0183_GEN as GEN
from ..custom_project_lib.nmea0183_sentences_test import NMEA0183_GEN_TEST as TEST

# [WINDOWS] Replace 'COMX' with the appropriate virtual COM port on your system
# serial_port = "COM1"
# [LINUX] Replace '/dev/ttyUSBX' with the appropriate serial port on your system
# serial_port = '/dev/ttyUSB0'

# Open the serial port

# lat and long in degree minutes format(DM) Between uk and ireland {Test}
latitude = 53.679746945954754
longitude = -5.167506462247125

def serialConnection(port: str):
    serial_port = port
    try:
        ser = serial.Serial(serial_port, 4800, timeout=1)
        print(f"Connected to {serial_port}")
    except serial.SerialException as e:
        print(f"Failed to connect to {serial_port}: {e}")
        exit()

    while True:
        # Use any sentences here and send them to OpenCPN with serial.write((sentence + '\r\n').encode())

        # Create a minimal GGA sentence with only latitude and longitude
        gga = GEN.gga(
                                    lat = latitude,
                                    long = longitude,
                                    fix_quality = 1,
                                    satellites = 10,
                                    horizontal_dilution_of_precision = 0.1,
                                    elevation_above_sea_level = 255.747,
                                    elevation_unit = "M",
                                    geoid = -32.00,
                                    geoid_unit = "M",
                                    age_of_correction_data_seconds = "01",
                                    correction_station_id = "0000")

        # gga = TEST.test_gga(latitude=latitude, longitude=longitude, print_sentence=True)
        # Send the NMEA sentence to the serial port
        ser.write(
            (gga + "\r\n").encode()
        )  # Ensure to add line ending (\r\n) for NMEA sentences

        # Increment the latitude and longitude for the next update
        latitude += -0.001
        longitude += -0.009

        # Wait for a few seconds before sending the next update
        time.sleep(0.5)

def socketConnection(hostip:str, portOpen:int):
    host = hostip  # OpenCPN's IP address
    port = portOpen  # OpenCPN's default port for NMEA data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print("Connection successful")
        except Exception as e:
            print(f"Connection failed: {e}")
        s.connect((host, port))
        # Create a minimal GGA sentence with only latitude and longitude
        gga = GEN.gga(  lat = latitude,
                        long = longitude,
                        fix_quality = 1,
                        satellites = 10,
                        horizontal_dilution_of_precision = 0.1,
                        elevation_above_sea_level = 255.747,
                        elevation_unit = "M",
                        geoid = -32.00,
                        geoid_unit = "M",
                        age_of_correction_data_seconds = "01",
                        correction_station_id = "0000")

        # gga = TEST.test_gga(latitude=latitude, longitude=longitude, print_sentence=True)
        # Send the NMEA sentence to the serial port
        s.sendall((gga + "\r\n").encode())  # Ensure to add line ending (\r\n) for NMEA sentences


socketConnection("ip", 10110)
# serialConnection("COM1")