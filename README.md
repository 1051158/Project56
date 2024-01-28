### Handleiding

There are 2 possibilities to connect this code to OpenCPN. Either via UDP or Serial. <br>
Please look at demo.py in the demo directory to diffrentiate which data is required.

## Set-up
For connecting via Udp or serial, we need to set up OpenCPN first. If you don't have OpenCPN, please download via this link: https://opencpn.org/OpenCPN/info/downloadopencpn.html
or just look up OpenCPN and go to the one with a url that looks like this https://opencpn.org/ then Downloads>OpenCPN Latest Release

Follow the instructions to install OpenCPN. When installed, you should be able to open the app.

## UDP
To use a UDP connection, first follow this path in the application Options(Gear icon)/Connections

Click on `Add connection` and so the following:
- Choose **Network**
- Choose for `Protocol` TCP/**UDP**/GPSD/Signal K
- Leave `Address` Empty(or 127.0.0.1 or localhost)
- `DataPort` can be empty(default **10110**) or choose any unoccupied one that you like
- `User Comment` is empty
- Leave `List position` as it be
- Check **Control checksum**
- Check **Receive input on this Port**
- For `Input filtering` you can choose **Ignore sentences** and leave the field under blank

Click **Apply**
Make sure that the Data Connection is enabled (Check top-left corner off each connection)

Then in the code that will send data to OpenCPN:
- OpenCPN and the code are on the same machine: put host's ip in the code as `127.0.0.1` or `localhost` and the same port as the one you've filled in when setting up OpenCPN
- OpenCPN and the code are on a different machine (same network): put host's ip in the code as the ip of the OpenCPN hosting machine, and the same port as the one you've filled in when setting up OpenCPN

To get the ip of a hosting machine, go to that machine, open the command prompt/powershell/terminal and do:

Windows: ```ipconfig```

MAC: System Settings/Network/Wi-Fi/Details... and look at your ip address

Linux: ```hostname -l``` or ```ifconfig```

Please only use IPv4.

## Serial
You need a virtual serial port emulator to make a port pair with one of them being the data sender(code) and the other is data receiver(OpenCPN).

To use a Serial connection, first follow this path in the application Options(Gear icon)/Connections

Click on `Add connection` and so the following:
- Choose **Serial**
- Choose for `DataPort` the latter port that was mentioned.
- Put `Protocol` as NMEA 0183
- `Baudrate` can be can be to your liking, but both code and openCPN should have the same valueddd
- Leave `List position` as it be
- `User Comment` is empty
- Check **Control checksum**
- Check **Receive input on this Port**
- For `Input filtering` you can choose **Ignore sentences** and leave the field under blank

## Dependencies

To ensure the proper functioning of this project, various libraries and frameworks are utilized in both the Arduino and Python components. Below is a detailed list of these dependencies:

### Arduino Dependencies
The following libraries are used in the `.ino` Arduino sketches:

- **Wire.h**: A library for I2C communication, commonly used for interfacing with sensors and devices.
- **Adafruit_GFX.h**: A graphics library used for drawing text, shapes, and images on small displays.
- **Adafruit_SSD1306.h**: A library specifically for controlling the Adafruit SSD1306 OLED display.
- **Arduino.h**: Standard Arduino library.

### Python Dependencies
These dependencies are included in the `.py` Python scripts:

- **dash**: A Python framework for building interactive web applications.
- **html, dcc (from dash)**: Components of Dash for creating HTML elements and interactive components.
- **plotly.express, plotly.graph_objects**: Plotly libraries for creating interactive plots and graphs.
- **pandas**: A data manipulation and analysis library.
- **multiprocessing**: A built-in Python module for parallel processing.
- **struct**: A module for converting between Python values and C structs.
- **serial**: A module for serial communication with devices.
- **pymongo**: A MongoDB driver for Python.
- **certifi**: A Python package for providing Mozilla's CA Bundle.
- **scipy.optimize**: A module for optimization and root finding.
- **numpy**: A package for scientific computing.
- **pynmea2**: A library for parsing NMEA 0183 sentences.
- **datetime (from datetime)**: A module for manipulating dates and times.
- **typing (Optional)**: A module for support of type hints.
- **socket**: A module for creating socket connections.
- **colorama**: A module for colored terminal text.
