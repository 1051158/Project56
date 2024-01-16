// Define constants
#define UWB_INDEX 0
#define TAG
#define FREQ_850K
#define UWB_TAG_COUNT 32

// Include libraries
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

// Define serial ports
#define SERIAL_LOG Serial
#define SERIAL_AT mySerial2

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
    // Set pin mode and initial state
    pinMode(RESET, OUTPUT);
    digitalWrite(RESET, HIGH);

    // Initialize serial ports
    SERIAL_LOG.begin(115200);
    SERIAL_AT.begin(115200, SERIAL_8N1, IO_RXD2, IO_TXD2);

    // Send AT command to check communication
    SERIAL_AT.println("AT");

    // Initialize I2C communication
    Wire.begin(I2C_SDA, I2C_SCL);
    delay(1000);

    // Initialize display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        SERIAL_LOG.println(F("SSD1306 allocation failed"));
        for (;;)
            ;
    }
    display.clearDisplay();

    // Show logo on display
    logoshow();

    // Send AT commands to configure the module
    sendData("AT?", 2000, 1);
    sendData("AT+RESTORE", 5000, 1);
    sendData(config_cmd(), 2000, 1);
    sendData(cap_cmd(), 2000, 1);
    sendData("AT+SETRPT=1", 2000, 1);
    sendData("AT+SAVE", 2000, 1);
    sendData("AT+RESTART", 2000, 1);
}

// Variable to store runtime
long int runtime = 0;

// Variables for AT command response handling
String response = "";
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

    // Read data from SERIAL_AT and handle AT command responses
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

// Function to display logo on the OLED display
void logoshow(void)
{
    display.clearDisplay();

    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println(F("MaUWB DW3000"));

    display.setCursor(0, 20);

    display.setTextSize(2);

    String temp = "";

#ifdef TAG
    temp = temp + "T" + UWB_INDEX;
#endif
#ifdef ANCHOR
    temp = temp + "A" + UWB_INDEX;
#endif
#ifdef FREQ_850K
    temp = temp + "   850k";
#endif
#ifdef FREQ_6800K
    temp = temp + "   6.8M";
#endif
    display.println(temp);

    display.setCursor(0, 40);

    temp = "Total: ";
    temp = temp + UWB_TAG_COUNT;
    display.println(temp);

    display.display();

    delay(2000);
}

// Function to send AT command and receive response
String sendData(String command, const int timeout, boolean debug)
{
    String response = "";

    SERIAL_LOG.println(command);
    SERIAL_AT.println(command);

    long int time = millis();

    while ((time + timeout) > millis())
    {
        while (SERIAL_AT.available())
        {
            char c = SERIAL_AT.read();
            response += c;
        }
    }

    if (debug)
    {
        SERIAL_LOG.println(response);
    }

    return response;
}

// Function to generate configuration AT command
String config_cmd()
{
    String temp = "AT+SETCFG=";

    temp = temp + UWB_INDEX;

#ifdef TAG
    temp = temp + ",0";
#endif
#ifdef ANCHOR
    temp = temp + ",1";
#endif

#ifdef FREQ_850K
    temp = temp + ",0";
#endif
#ifdef FREQ_6800K
    temp = temp + ",1";
#endif

    temp = temp + ",1";

    return temp;
}

// Function to generate capability AT command
String cap_cmd()
{
    String temp = "AT+SETCAP=";

    temp = temp + UWB_TAG_COUNT;

#ifdef FREQ_850K
    temp = temp + ",15";
#endif
#ifdef FREQ_6800K
    temp = temp + ",10";
#endif

    return temp;
}