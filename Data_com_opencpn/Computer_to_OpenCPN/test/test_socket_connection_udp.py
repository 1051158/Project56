import socket
import time

# Define OpenCPN address and port
print("--------------------------------------------------------------------------------")
opencpn_address = input("| > OpenCPN's IP address: ")  # Use the IP address of the laptop running OpenCPN
opencpn_port = int(input("| > OpenCPN's port: "))  # Use the port set in OpenCPN

# Open a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Example GGA data
gga_data = "$GPGGA,224456.000,5153.89950978450045,N,000425.12713876380202,E,1,10,0.1,255.747,M,-32.0,M,01,0000"
print("| [200] Sending GGA data to OpenCPN..., press Ctrl+C to stop")
while True:
    # Send GGA data to OpenCPN
    udp_socket.sendto(gga_data.encode(), (opencpn_address, opencpn_port))

    # Adjust the frequency of sending data according to your needs
    time.sleep(1)


