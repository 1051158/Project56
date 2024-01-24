import socket
import time

class SOCKET_CONNECTION:
    data = ""

    def __init__(self) -> None:
        pass
    
    def change_data(self, data: str) -> None:
        self.data = data

    def tcp(self, *, delay: float):
        print("--------------------------------------------------------------------------------")
        print("| TCP Socket Connection to OpenCPN")
        print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
        print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
        print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
        host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
        port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data

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
                gga = self.data
                # Send GGA data to OpenCPN
                tcp_socket.sendall(gga.encode())

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

    def udp(self, *, delay: float): #hostip:str, portOpen:int
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
                gga = self.data
            
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