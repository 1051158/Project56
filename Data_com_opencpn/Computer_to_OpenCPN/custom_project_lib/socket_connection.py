import socket
import time
'''
Hello, this is a socket connection class for OpenCPN.
'''
class SOCKET_CONNECTION:
    __data = None
    __socket = None
    __protocol = None
    __openCPN_host = None
    __openCPN_port = None

    def __init__(self) -> None:
        self.__data = ""
        self.__socket = None
        self.__protocol = ""
        self.__openCPN_host = ""
        self.__openCPN_port = 0
    
    def change_data(self, data: str) -> None:
        self.__data = data

    '''
    TCP Socket Connection to OpenCPN
    '''
    def tcp(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("| TCP Socket Connection to OpenCPN")
        print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
        print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
        print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
        self.__openCPN_host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
        self.__openCPN_port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data
        print("--------------------------------------------------------------------------------")

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__protocol = "TCP"

        try:
            # Connect to OpenCPN
            self.__socket.connect((self.__openCPN_host, self.__openCPN_port))
            print("| [~~~~~~~] TCP Socket connection is established!")
            print("--------------------------------------------------------------------------------")
        except ConnectionRefusedError as cre:
            print(f"| [X] Connection to OpenCPN at {self.__openCPN_host}:{self.__openCPN_port} was refused.")
            print(f"| [X] Error: {cre}")
            print("--------------------------------------------------------------------------------")
            self.__socket.close()
            exit()
        except Exception as e:
            print(f"| [X] An error occurred: {e}")
            print("--------------------------------------------------------------------------------")
            self.__socket.close()
            exit()

    '''
    UDP Socket Connection to OpenCPN
    '''
    def udp(self) -> None:
        print("--------------------------------------------------------------------------------")
        print("| UDP Socket Connection to OpenCPN")
        print("| When using on Local machine, use either localhost or 127.0.0.1 as host")
        print("| When using on Remote machine, use the IP address of the machine running OpenCPN")
        print("| Please use the same port as the one set in OpenCPN, or use the default port 10110")
        self.__openCPN_host = input("| > OpenCPN/Host's IP-address: ")  # OpenCPN's IP address/HOST computer's ip address
        self.__openCPN_port = int(input("| > Listening port: "))  # OpenCPN's default port for NMEA data
        print("--------------------------------------------------------------------------------")

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__protocol = "UDP"

        print("| [~~~~~~~] UDP Socket connection is established!")
        print("--------------------------------------------------------------------------------")

    '''
    Close the socket connection
    '''
    def close(self) -> None:
        print("| [----~~~] Closing Socket Connection")
        print("--------------------------------------------------------------------------------")
        try:
            self.__socket.close()
            print("| [-------] Socket connection is closed!")
            print("--------------------------------------------------------------------------------")
        except Exception as e:
            print(f"| [X] Error: {e}")
            print("--------------------------------------------------------------------------------")
            exit()

    '''
    Send the data to OpenCPN
    '''
    def send_data(self) -> str:
        try: # Send the NMEA sentence to the serial port and catch any errors
            sentence = self.__data
            # sentence = self.data + "\r\n"
        
            # Send the NMEA sentence to OpenCPN via UDP/TCP
            if self.__protocol == "TCP":
                self.__socket.sendall(sentence.encode())
            elif self.__protocol == "UDP":
                self.__socket.sendto(sentence.encode(), (self.__openCPN_host, self.__openCPN_port))
            self.__data = "" # Clear the data

            return sentence.replace("\r\n", "")

        except Exception as e:
            print(f"| [X] Error: {e}")
            print(f"| Host: {self.__openCPN_host}, Port: {self.__openCPN_port}")
            print("--------------------------------------------------------------------------------")
            exit()

    '''
    Close the socket connection when the object is deleted
    '''
    def __del__(self) -> None:
        self.close()
