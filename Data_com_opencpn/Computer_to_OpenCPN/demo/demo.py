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

# lat and long in degree minutes format(DM) at RDM Rotterdam, AquaLabs{Test}
latitude = [51.89832516307501]
longitude = [4.418785646063367]

def serialConnection():
    print("--------------------------------------------------------------------------------")
    print("| Serial Connection to OpenCPN")
    print("| Please use a different port than the one used by OpenCPN, because")
    print("|   OpenCPN will not be able to use the same port for input and output")
    print("| Please use the same baud rate as the one set in OpenCPN, or use the default baud rate 4800")
    serial_port = input("| > Serial Port: ")  # OpenCPN's default port for NMEA data
    baud_rate = int(input("| > Baud Rate: "))  # OpenCPN's default port for NMEA data
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"| [200] Connected to {serial_port}")
    except serial.SerialException as e:
        print(f"| [X] Failed to connect to {serial_port}: {e}")
        print("--------------------------------------------------------------------------------")
        exit()

    while True:
        # Use any sentences here and send them to OpenCPN with serial.write((sentence + '\r\n').encode())
        global latitude
        global longitude
        # Create a minimal GGA sentence with only latitude and longitude
        gga = GEN.gga(  lat = latitude[0],
                        long = longitude[0],
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
        latitude[0] += -0.001
        longitude[0] += -0.009

        # Wait for a few seconds before sending the next update
        time.sleep(0.5)

def socketConnection_udp(*, delay: float): #hostip:str, portOpen:int
    print("--------------------------------------------------------------------------------")
    print("| UDP Socket Connection to OpenCPN")
    print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
    print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
    print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
    host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("| [200] UDP Socket connection is established!")
    while True:
        # Create a minimal GGA sentence with only latitude and longitude
        global latitude
        global longitude
        gga = GEN.gga(  lat = latitude[0],
                        long = longitude[0],
                        fix_quality = 1,
                        satellites = 10,
                        horizontal_dilution_of_precision = 0.1,
                        elevation_above_sea_level = 255.747,
                        elevation_unit = "M",
                        geoid = -32.00,
                        geoid_unit = "M",
                        age_of_correction_data_seconds = "01",
                        correction_station_id = "0000") + "\r\n" # Ensure to add line ending (\r\n) for NMEA sentences
        
        try: # Send the NMEA sentence to the serial port and catch any errors
            udp_socket.sendto(gga.encode(), (host, port))
            # Increment the latitude and longitude for the next update
            latitude[0] += -0.001
            longitude[0] += -0.009
        except Exception as e:
            print(f"| [X] Error: {e}")
            print(f"| Host: {host}, Port: {port}")
            print("--------------------------------------------------------------------------------")
            exit()

        time.sleep(delay)
        

# Use either Serial or Socket connection
socketConnection_udp(delay=0.5)
# serialConnection()