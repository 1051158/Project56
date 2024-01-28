### Handleiding

There are 2 possibilities to connect this code to OpenCPN. Either via UDP or TCP. <br>

## Set-up
For connecting via Udp or TCP, we need to set up OpenCPN first. If you don't have OpenCPN, please download via this link: https://opencpn.org/OpenCPN/info/downloadopencpn.html
or just look up OpenCPN and go to the one with a url that looks like this https://opencpn.org/ then Downloads>OpenCPN Latest Release

Follow the instructions to install OpenCPN. When installed, you should be able to open the app.

## TCP/UDP
To use a TCP or UDP connection, first follow this path in the application Options(Gear icon)/Connections

Click on `Add connection` and so the following:
- Choose **Network**
- Choose for `Protocol` **TCP**/**UDP**/GPSD/Signal K
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

Please only use **IPv4**.

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

## Installation

This project involves both Arduino and Python components. Follow these steps to set up each part of the project.

### Arduino Setup

1. **Install the Arduino IDE**: If you haven't already, download and install the Arduino IDE from [the official Arduino website](https://www.arduino.cc/en/Main/Software).

2. **Connect Your Arduino Device**: Connect your Arduino board to your computer using a USB cable.

3. **Install Required Libraries**:
   - Open the Arduino IDE.
   - Go to `Sketch` > `Include Library` > `Manage Libraries...`.
   - Search for and install the following libraries:
     - `Wire`
     - `Adafruit GFX Library`
     - `Adafruit SSD1306`

4. **Load the Arduino Sketch**:
   - Open the `.ino` file for your project in the Arduino IDE.
   - Select the correct board and port under `Tools`.

5. **Upload the Sketch**:
   - Click on the upload button in the Arduino IDE to upload the sketch to your Arduino board.

### Python Environment Setup

1. **Install Python**: Ensure that Python is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).

2. **Set Up a Virtual Environment (Optional but Recommended)**:
   - Open a terminal or command prompt.
   - Navigate to your project directory.
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment:
     - On Windows: `venv\Scripts\activate`
     - On macOS/Linux: `source venv/bin/activate`

3. **Install Python Dependencies**:
   - While in your project directory and with the virtual environment activated, run:
     ```
     pip install dash pandas plotly scipy pymongo serial certifi pynmea2 colorama
     ```

4. **Running Python Scripts**:
   - Navigate to the directory containing the Python scripts.
   - Run the scripts using Python. For example:
     ```
     python dashapp.py
     ```
   - For `position.py`, due to it's using the local packages in custom_project_lib, a different way of running the script is required:
      ```
      python -m Data_com_opencpn.Computer_to_OpenCPN.src.position
      ```
      or
      ```
      python3 -m Data_com_opencpn.Computer_to_OpenCPN.src.position
      ```
      This is only for when the project is opened at its root(Project56 directory). When you open the project at any lower branches, please adjust the package path accordingly. For example, when the project is opened at `Project56/Data_com_opencpn/Computer_to_OpenCPN/src`, then the bash will look like this:
      ```
      python3 -m position
      ```

### Post-Installation Checks

- After installing both the Arduino and Python components, ensure that all devices are correctly connected and the software is running without errors.
- Check that the Arduino board is communicating correctly with the Python scripts, if required by your project setup.

## Configuration

Proper configuration of both hardware and software components is essential for the optimal functioning of the project. Below are the detailed steps for setting up MongoDB, which is used for data storage and management.

### Setting Up MongoDB

1. **Install MongoDB**:
   - Download and install MongoDB from [the official MongoDB website](https://www.mongodb.com/try/download/community).
   - Follow the installation instructions specific to your operating system.

2. **Start the MongoDB Service**:
   - On Windows, MongoDB is installed as a service and will start automatically.
   - On macOS and Linux, you may need to start MongoDB manually. Typically, this can be done with a command like `mongod` in your terminal.

3. **Verify MongoDB Installation**:
   - Open a terminal or command prompt.
   - Type `mongo` and press Enter. This opens the MongoDB shell if MongoDB is running correctly.

4. **Create a Database and Collection**:
   - In the MongoDB shell, create a new database using `use <database_name>`, replacing `<database_name>` with your preferred database name.
   - Create a collection within your database by executing `db.createCollection("<collection_name>")`, replacing `<collection_name>` with a name for your collection.

5. **Configure MongoDB in Your Python Script**:
   - In your Python script, ensure you have the pymongo library installed (`pip install pymongo`).
   - Use the following template to connect to your MongoDB database:
     ```python
     from pymongo import MongoClient
     import certifi

     client = MongoClient('mongodb://localhost:27017/', tlsCAFile=certifi.where())
     db = client["<database_name>"]
     collection = db["<collection_name>"]
     ```
   - Replace `<database_name>` and `<collection_name>` with the names you chose earlier.

6. **Setting Up MongoDB Authentication** (Optional but Recommended):
   - For production environments, it's important to enable authentication.
   - Create an admin user and then a user for your database with appropriate permissions.
   - More details on setting up authentication can be found in the [MongoDB Security Checklist](https://docs.mongodb.com/manual/administration/security-checklist/).

## Run

### Step 1: run position.py
   - Use the following command: python3 -m Data_com_opencpn.Computer_to_OpenCPN.src.position.py
### Step 2: run dashapp.py
   - Use the following command: python3 dashapp.py
