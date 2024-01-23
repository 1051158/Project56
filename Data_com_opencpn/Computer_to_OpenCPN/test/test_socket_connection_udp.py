import socket
import time

# Define OpenCPN address and port
opencpn_address = '127.0.0.1'  # Use the IP address of the laptop running OpenCPN
opencpn_port = 10110

# Open a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Example GGA data
gga_data = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
print("Sending GGA data to OpenCPN..., press Ctrl+C to stop")
while True:
    # Send GGA data to OpenCPN
    udp_socket.sendto(gga_data.encode(), (opencpn_address, opencpn_port))

    # Adjust the frequency of sending data according to your needs
    time.sleep(1)
