#
#
# DON"T USE
#
#
import socket
import time

latitude = 63.40206806724627
longitude = -18.733945285880537

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 450))  # Replace with your desired IP and port
server_socket.listen(1)

client_socket, addr = server_socket.accept()

while True:
    data = f'GPGGA,123519,{latitude},N,{longitude},W,1,08,0.9,545.4,M,46.9,M,,*47\r\n'  # NMEA sentence
    client_socket.sendall(data.encode())
    time.sleep(1)  # Update frequency in seconds
