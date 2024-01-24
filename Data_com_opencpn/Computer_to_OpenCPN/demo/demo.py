#
# USE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This script is used to send NMEA sentences to OpenCPN
# Always pair a nmea sentence with a serial.write() command
#

import serial
import socket
import time
# import paho.mqtt.publish as publish
# import paho.mqtt.client as mqttClient
from ..custom_project_lib.nmea0183_sentences import NMEA0183_GEN as GEN
from ..custom_project_lib.nmea0183_sentences_test import NMEA0183_GEN_TEST as TEST

# [WINDOWS] Replace 'COMX' with the appropriate virtual COM port on your system
# serial_port = "COM1"
# [LINUX] Replace '/dev/ttyUSBX' with the appropriate serial port on your system
# serial_port = '/dev/ttyUSB0'

# lat and long in degree minutes format(DM) at RDM Rotterdam, AquaLabs{Test}
latitude = [51.89832516307501]
longitude = [4.418785646063367]

def serialConnection(*, delay: float):
    print("--------------------------------------------------------------------------------")
    print("| Serial Connection to OpenCPN")
    print("| Please use a different port than the one used by OpenCPN, because")
    print("|   OpenCPN will not be able to use the same port for input and output")
    print("| Please use the same baud rate as the one set in OpenCPN, or use the default baud rate 4800")
    serial_port = input("| > Serial Port: ")  # OpenCPN's default port for NMEA data
    baud_rate = int(input("| > Baud Rate: "))  # OpenCPN's default port for NMEA data
    increment = input("| > Increment latitude and longitude? (y/n): ") == "n"

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
        if increment == "y":
            latitude[0] += -0.001
            longitude[0] += -0.009

        # Wait for a few seconds before sending the next update
        time.sleep(delay)

def socketConnection_udp(*, delay: float): #hostip:str, portOpen:int
    print("--------------------------------------------------------------------------------")
    print("| UDP Socket Connection to OpenCPN")
    print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
    print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
    print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
    host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data
    increment = input("| > Increment latitude and longitude? (y/n): ") == "n"

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("| [200] UDP Socket connection is established!")

    try: # Send the NMEA sentence to the serial port and catch any errors
                
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
                            correction_station_id = "0001") + "\r\n" # Ensure to add line ending (\r\n) for NMEA sentences
        
            # Send the NMEA sentence to OpenCPN via UDP
            udp_socket.sendto(gga.encode(), (host, port))
            # Increment the latitude and longitude for the next update
            if increment == "y":
                latitude[0] += -0.001
                longitude[0] += -0.009

            time.sleep(delay)

    except Exception as e:
        print(f"| [X] Error: {e}")
        print(f"| Host: {host}, Port: {port}")
        exit()
    finally:
        udp_socket.close()
        print("| [_] Socket closed.")
        print("--------------------------------------------------------------------------------")

    

def socketConnection_tcp(*, delay: float):
    print("--------------------------------------------------------------------------------")
    print("| TCP Socket Connection to OpenCPN")
    print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
    print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
    print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
    host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data
    increment = input("| > Increment latitude and longitude? (y/n): ") == "n"

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to OpenCPN
        tcp_socket.connect((host, port))
        print("| [200] TCP Socket connection is established!")
    except ConnectionRefusedError as cre:
        print(f"| [X] Connection to OpenCPN at {host}:{port} was refused.")
        print(f"| [X] Error: {cre}")
        print("--------------------------------------------------------------------------------")
        tcp_socket.close()
        exit()
    except Exception as e:
        print(f"| [X] An error occurred: {e}")
        print("--------------------------------------------------------------------------------")
        tcp_socket.close()
        exit()

    try: 
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
                            correction_station_id = "0000") 
            # + "\r\n" # Ensure to add line ending (\r\n) for NMEA sentences
            # Send GGA data to OpenCPN
            tcp_socket.sendall(gga.encode())

            # Increment the latitude and longitude for the next update
            if increment == "y":
                latitude[0] += -0.001
                longitude[0] += -0.009

            # Adjust the frequency of sending data according to your needs
            time.sleep(delay)

    except Exception as e:
        print(f"| [X] Error: {e}")
        print(f"| Host: {host}, Port: {port}")
        print("--------------------------------------------------------------------------------")
        exit()
    finally:
        tcp_socket.close()
        ("[_] Socket closed.")

def socketConnection_tcp_1s(*, delay: float, sentence: str = None, host: str = None, port: int = None, increment: str = None):
    print("--------------------------------------------------------------------------------")
    print("| TCP Socket Connection to OpenCPN")
    print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
    print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
    print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
    host = host or input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    port = port or int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data
    increment = increment or input("| > Increment latitude and longitude? (y/n): ") == "n"

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to OpenCPN
        tcp_socket.connect((host, port))
        print("| [200] TCP Socket connection is established!")
    except ConnectionRefusedError as cre:
        print(f"| [X] Connection to OpenCPN at {host}:{port} was refused.")
        print(f"| [X] Error: {cre}")
        print("--------------------------------------------------------------------------------")
        tcp_socket.close()
        exit()
    except Exception as e:
        print(f"| [X] An error occurred: {e}")
        print("--------------------------------------------------------------------------------")
        tcp_socket.close()
        exit()

    try: 
        # Create a minimal GGA sentence with only latitude and longitude
        global latitude
        global longitude
        gga = (str(sentence) + "\n\r" if sentence is not None else None) or GEN.gga(  lat = latitude[0],
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
        # + "\r\n" # Ensure to add line ending (\r\n) for NMEA sentences
        # Send GGA data to OpenCPN
        tcp_socket.sendall(gga.encode())

        # Increment the latitude and longitude for the next update
        if increment == "y":
            latitude[0] += -0.001
            longitude[0] += -0.009

    except Exception as e:
        print(f"| [X] Error: {e}")
        print(f"| Host: {host}, Port: {port}")
        print("--------------------------------------------------------------------------------")
        exit()
    finally:
        tcp_socket.close()
        ("[_] Socket closed.")

        
def mqttConnectionPublisher(*, delay: float):
    print("--------------------------------------------------------------------------------")
    print("| MQTT Connection to OpenCPN as Publisher")
    print("| Please use the same topic as the Subscriber, or use the default topic topic/gga")
    print("| Please use the MQTT borker's IP address (host)")
    print("| Please use the MQTT borker's port (port), default is 1883")
    mqtt_broker_ip = input("| > MQTT Broker's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    topic = input("| > Topic: ")  # OpenCPN's default port for NMEA data
    increment = input("| > Increment latitude and longitude? (y/n): ") == "n"

    print("| [200] MQTT Publisher's data is sent")
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
                        correction_station_id = "0000")
        publish.single(f"topic/{topic}", gga, hostname=mqtt_broker_ip)

        # Increment the latitude and longitude for the next update
        if increment == "y":
            latitude[0] += -0.001
            longitude[0] += -0.009

        time.sleep(delay)  # Adjust the interval as needed

def mqttConnectionSubsciber(*, delay: float):
    # Define MQTT broker details
    print("--------------------------------------------------------------------------------")
    print("| MQTT Connection to OpenCPN as Subscriber")
    broker_address = input("| > MQTT Broker's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    broker_port = int(input("| > MQTT Broker's port: "))  # OpenCPN's default port for NMEA data
    topic = f"topic/{input('| > Topic: ')}" # OpenCPN's default port for NMEA data
    host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
    port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribe to the GGA topic when connected
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        # Parse and process the GGA data
        gga_data = msg.payload.decode('utf-8')
        process_gga_data(gga_data)

    def process_gga_data(gga_data):
        # You can customize this function to handle the GGA data as needed
        print("Received GGA data: {}".format(gga_data))
        # socketConnection_tcp_1s(delay=0.5, sentence=gga_data, host=host, port=port, increment="n")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(gga_data.encode('utf-8'))
            s.close()
            s.shutdown(socket.SHUT_RDWR)

    # Create an MQTT client instance
    client = mqttClient.Client()

    # Set up the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(broker_address, broker_port, 60)

    # Start the MQTT client loop
    client.loop_forever()




# Use either Serial or Socket connection
# serialConnection(delay = 0.5)        
# socketConnection_udp(delay=0.5)
# socketConnection_tcp(delay=0.5)
# mqttConnectionPublisher(delay=0.5) #incomplete
# mqttConnectionSubsciber(delay=0.5) #incomplete

# Use this to (root is Project56 directory): python -m Data_com_opencpn.Computer_to_OpenCPN.demo.demo