// Include necessary libraries
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

// Define serial ports
#define SERIAL_LOG Serial
#define SERIAL_AT mySerial2

// Define hardware serial port
HardwareSerial SERIAL_AT(2);

// Define pin numbers
#define RESET 32
#define IO_RXD2 18
#define IO_TXD2 19
#define I2C_SDA 4
#define I2C_SCL 5

// Create an instance of the SSD1306 display
Adafruit_SSD1306 display(128, 64, &Wire, -1);

// Setup function
void setup()
{
    // Set RESET pin as output and set it high
    pinMode(RESET, OUTPUT);
    digitalWrite(RESET, HIGH);

    // Initialize serial communication for logging
    SERIAL_LOG.begin(115200);

    // Initialize serial communication for AT commands
    SERIAL_AT.begin(115200, SERIAL_8N1, IO_RXD2, IO_TXD2);

    // Send AT command to check communication
    SERIAL_AT.println("AT");

    // Initialize I2C communication
    Wire.begin(I2C_SDA, I2C_SCL);
    delay(1000);

    // Initialize the display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        SERIAL_LOG.println(F("SSD1306 allocation failed"));
        for (;;)
            ;
    }
    display.clearDisplay();

    // Show the logo on the display
    logoshow();

    // Send AT commands to configure the module
    sendData("AT?", 2000, 1);
    sendData("AT+RESTORE", 5000, 1);
    sendData("AT+SETCFG=0,1,0,1", 2000, 1);
    sendData("AT+SETCAP=32,15", 2000, 1);
    sendData("AT+SETRPT=1", 2000, 1);
    sendData("AT+SAVE", 2000, 1);
    sendData("AT+RESTART", 2000, 1);
}

// Variable to store the runtime
long int runtime = 0;

// Variable to store the AT command response
String response = "";

// Variable to store the AT command header
String rec_head = "AT+RANGE";

// Loop function
void loop()
{
    // Forward data from SERIAL_LOG to SERIAL_AT
    while (SERIAL_LOG.available() > 0)
    {
        SERIAL_AT.write(SERIAL_LOG.read());
        yield();
    }

    // Read data from SERIAL_AT and process the response
    while (SERIAL_AT.available() > 0)
    {
        char c = SERIAL_AT.read();

        if (c == '\r')
            continue;
        else if (c == '\n' || c == '\r')
        {
            SERIAL_LOG.println(response);
            response = "";
        }
        else
            response += c;
    }
}

// Function to display the logo on the OLED display
void logoshow(void)
{
    display.clearDisplay();

    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println(F("MaUWB DW3000"));
    display.setCursor(0, 20);
    display.println(F("with STM32 AT Command"));

    display.setTextSize(2);
    display.setCursor(0, 40);
    display.println(F("A0"));
    display.display();
    delay(2000);
}

// Function to send AT command and receive response
String sendData(String command, const int timeout, boolean debug)
{
    String response = "";

    // Send command to SERIAL_LOG and SERIAL_AT
    SERIAL_LOG.println(command);
    SERIAL_AT.println(command);

    // Record the current time
    long int time = millis();

    // Wait for response within the specified timeout
    while ((time + timeout) > millis())
    {
        while (SERIAL_AT.available())
        {
            char c = SERIAL_AT.read();
            response += c;
        }
    }

    // Print the response if debug mode is enabled
    if (debug)
    {
        SERIAL_LOG.println(response);
    }

    return response;
}
