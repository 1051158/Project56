import socket
import time

# Define OpenCPN address and port
opencpn_address = '127.0.0.1'  # Use the IP address of the laptop running OpenCPN
opencpn_port = 10110

# Open a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to OpenCPN
tcp_socket.connect((opencpn_address, opencpn_port))

# Example GGA data
gga_data = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"

while True:
    # Send GGA data to OpenCPN
    tcp_socket.sendall(gga_data.encode())

    # Adjust the frequency of sending data according to your needs
    time.sleep(1)
