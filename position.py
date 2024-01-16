# Import libraries
import pygame
import serial
import serial.tools.list_ports
import json
import time
import math
from pymongo import MongoClient
import certifi


# Define color constants
RED = [255, 0, 0]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

uri = "mongodb+srv://aleniriskic:0hZpyfFParfakoMe@aquabotcluster.lmorwiv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client.RangeData  # Replace with your database name
collection = db.trip1


class UWB:
    def __init__(self, name, type):
        """
        Initializes the UWB object with the given name and type.
        Sets the initial coordinates to (0, 0), status to False, and an empty list.
        Determines the color based on the type.
        """
        self.name = name
        self.type = type
        self.x = 0
        self.y = 0
        self.status = False
        self.list = []

        if self.type == 1:
            self.color = RED
        else:
            self.color = BLACK

    def set_location(self, x, y):
        """
        Sets the location of the UWB object to the given coordinates (x, y).
        """
        self.x = x
        self.y = y
        self.status = True

    def cal(self):
        """
        Calculates the location of the UWB object based on the received range data.
        Uses the three-point algorithm to estimate the coordinates.
        """
        count = 0
        anc_id_list = []
        for range in self.list:
            if range != 0:
                anc_id_list.append(count)
                count = count + 1

        if count >= 3:
            x = 0.0
            y = 0.0

            temp_x, temp_y = self.three_point_uwb(anc_id_list[0], anc_id_list[1])

            x += temp_x
            y += temp_y

            temp_x, temp_y = self.three_point_uwb(anc_id_list[0], anc_id_list[2])

            x += temp_x
            y += temp_y

            temp_x, temp_y = self.three_point_uwb(anc_id_list[2], anc_id_list[1])

            x += temp_x
            y += temp_y

            x = int(x / 3)
            y = int(y / 3)

            self.set_location(x, y)
            self.status = True

    def three_point_uwb(self, a_id, b_id):
        """
        Calculates the coordinates of the UWB object using the three-point algorithm
        with the given anchor IDs a_id and b_id.
        """
        x, y = self.three_point(
            anc[a_id].x,
            anc[a_id].y,
            anc[b_id].x,
            anc[b_id].y,
            self.list[a_id],
            self.list[b_id],
        )

        return x, y

    def three_point(self, x1, y1, x2, y2, r1, r2):
        """
        Calculates the coordinates of the UWB object using the three-point algorithm
        with the given anchor coordinates (x1, y1), (x2, y2) and range values r1, r2.
        """
        temp_x = 0.0
        temp_y = 0.0
        p2p = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
        p2p = math.sqrt(p2p)

        if r1 + r2 <= p2p:
            temp_x = x1 + (x2 - x1) * r1 / (r1 + r2)
            temp_y = y1 + (y2 - y1) * r1 / (r1 + r2)
        else:
            dr = p2p / 2 + (r1 * r1 - r2 * r2) / (2 * p2p)
            temp_x = x1 + (x2 - x1) * dr / p2p
            temp_y = y1 + (y2 - y1) * dr / p2p

        return temp_x, temp_y


def get_com_port():
    """
    Returns the COM port selected by the user.
    """
    ports = serial.tools.list_ports.comports()
    if len(ports) == 0:
        print("No COM ports available")
        return None

    print("Available COM Ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")

    port_index = -1
    while port_index < 0 or port_index >= len(ports):
        try:
            port_index = int(input("Select COM port number: "))
        except ValueError:
            print("Please enter a valid number")

    return ports[port_index].device


def draw_uwb(uwb):
    """
    Draws the UWB object on the screen.
    """
    pixel_x = int(uwb.x * cm2p + x_offset)
    pixel_y = SCREEN_Y - int(uwb.y * cm2p + y_offset)

    if uwb.status:
        r = 10

        temp_str = uwb.name + " (" + str(uwb.x) + "," + str(uwb.y) + ")"

        font = pygame.font.SysFont("Consola", 24)
        surf = font.render(temp_str, True, uwb.color)
        screen.blit(surf, [pixel_x, pixel_y])

        pygame.draw.circle(screen, uwb.color, [pixel_x + 20, pixel_y + 50], r, 0)


def read_data():
    """
    Reads the data from the serial port, updates the UWB objects, and uploads the data to MongoDB.
    """
    line = ser.readline().decode("UTF-8").replace("\n", "")

    try:
        data = json.loads(line)
        print(data)
        print(data["id"])

        tag[data["id"]].list = data["range"]
        tag[data["id"]].cal()

        # Add anchor coordinates to data
        data["anchor_coordinates"] = [
            {"x": A0X, "y": A0Y},
            {"x": A1X, "y": A1Y},
            {"x": A2X, "y": A2Y},
            {"x": A3X, "y": A3Y},
        ]

        # Insert data into MongoDB
        collection.insert_one(data)

    except ValueError:
        print("[LOG]" + line)


def fresh_page():
    """
    Clears the screen and redraws the UWB objects.
    """
    runtime = time.time()
    screen.fill(WHITE)
    for uwb in anc:
        draw_uwb(uwb)
    for uwb in tag:
        draw_uwb(uwb)

    pygame.draw.line(screen, BLACK, (CENTER_X_PIEXL, 0), (CENTER_X_PIEXL, SCREEN_Y), 1)
    pygame.draw.line(screen, BLACK, (0, CENTER_Y_PIEXL), (SCREEN_X, CENTER_Y_PIEXL), 1)

    pygame.display.flip()

    print("Fresh Over, Use Time:")
    print(time.time() - runtime)


def distance(x1, y1, x2, y2):
    """
    Calculates the distance between two points.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Set up the pygame screen
SCREEN_X = 800
SCREEN_Y = 800
pygame.init()
screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

# Set up the serial port
ser = serial.Serial(get_com_port(), 115200)

# Initialize the anchor and tag UWB objects
anc = []
tag = []
anc_count = 4
tag_count = 8

# Define the anchor coordinates
A0X, A0Y = 0, 0
A1X, A1Y = 1000, 0
A2X, A2Y = 1000, 1000
A3X, A3Y = 0, 1000

# Calculate the center coordinates and maximum range
CENTER_X = int((A0X + A1X + A2X) / 3)
CENTER_Y = int((A0Y + A1Y + A2Y) / 3)
r0 = distance(A0X, A0Y, CENTER_X, CENTER_Y)
r1 = distance(A1X, A1Y, CENTER_X, CENTER_Y)
r2 = distance(A2X, A2Y, CENTER_X, CENTER_Y)
r3 = distance(A3X, A3Y, CENTER_X, CENTER_Y)
r = max(r0, r1, r2, r3)

# Calculate the conversion factor from centimeters to pixels
cm2p = SCREEN_X / 2 * 0.9 / r

# Calculate the offset for centering the UWB objects on the screen
x_offset = SCREEN_X / 2 - CENTER_X * cm2p
y_offset = SCREEN_Y / 2 - CENTER_Y * cm2p

# Calculate the pixel coordinates of the center point
CENTER_X_PIEXL = CENTER_X * cm2p + x_offset
CENTER_Y_PIEXL = CENTER_Y * cm2p + y_offset

# Create the anchor and tag UWB objects
for i in range(anc_count):
    name = "ANC " + str(i)
    anc.append(UWB(name, 0))
for i in range(tag_count):
    name = "TAG " + str(i)
    tag.append(UWB(name, 1))

# Set the initial locations of the anchor UWB objects
anc[0].set_location(A0X, A0Y)
anc[1].set_location(A1X, A1Y)
anc[2].set_location(A2X, A2Y)
anc[3].set_location(A3X, A3Y)

# Clear the screen and draw the UWB objects
fresh_page()

# Start the data reading loop
ser.write("begin".encode("UTF-8"))
ser.reset_input_buffer()
runtime = time.time()

while True:
    read_data()
    if (time.time() - runtime) > 0.5:
        fresh_page()
        runtime = time.time()
        ser.reset_input_buffer()
