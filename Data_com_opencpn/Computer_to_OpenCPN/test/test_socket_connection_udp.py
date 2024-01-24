import socket
import time

# Example GGA data
gga_data = "$GPGGA,224456.000,5153.89950978450045,N,000425.12713876380202,E,1,10,0.1,255.747,M,-32.0,M,01,0000"

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

    try: # Send the NMEA sentence to the serial port and catch any errors
                
        while True:
            # Create a minimal GGA sentence with only latitude and longitude
            global latitude
            global longitude
            gga = gga_data + "\r\n" # Ensure to add line ending (\r\n) for NMEA sentences
        
            # Send the NMEA sentence to OpenCPN via UDP
            udp_socket.sendto(gga.encode(), (host, port))

            time.sleep(delay)
    except Exception as e:
        print(f"| [X] Error: {e}")
        print(f"| Host: {host}, Port: {port}")
        exit()
    finally:
        udp_socket.close()
        print("| [_] Socket closed.")
        print("--------------------------------------------------------------------------------")

socketConnection_udp(delay=0.5)

