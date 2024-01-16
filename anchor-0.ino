// Include necessary libraries
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

// Define hardware serial object
HardwareSerial mySerial2(2);

// Define pin numbers
#define RESET 32
#define IO_RXD2 18
#define IO_TXD2 19
#define I2C_SDA 4
#define I2C_SCL 5

// Create SSD1306 display object
Adafruit_SSD1306 display(128, 64, &Wire, -1);

// Setup function
void setup()
{
    // Set RESET pin as output and set it high
    pinMode(RESET, OUTPUT);
    digitalWrite(RESET, HIGH);

    // Start serial communication
    Serial.begin(115200);

    // Print initial message
    Serial.print(F("Hello! ESP32-S3 AT command V1.0 Test"));

    // Start serial communication on mySerial2
    mySerial2.begin(115200, SERIAL_8N1, IO_RXD2, IO_TXD2);

    // Send "AT" command to mySerial2
    mySerial2.println("AT");

    // Start I2C communication
    Wire.begin(I2C_SDA, I2C_SCL);

    // Delay for 1 second
    delay(1000);

    // Initialize SSD1306 display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ;
    }

    // Clear the display
    display.clearDisplay();

    // Show logo on the display
    logoshow();
}

// Variable to store runtime
long int runtime = 0;

// Variables for response handling
String response = "";
String rec_head = "AT+RANGE";

// Loop function
void loop()
{
    // Read data from Serial and send it to mySerial2
    while (Serial.available() > 0)
    {
        mySerial2.write(Serial.read());
        yield();
    }

    // Read data from mySerial2 and process it
    while (mySerial2.available() > 0)
    {
        char c = mySerial2.read();

        // Skip carriage return characters
        if (c == '\r')
            continue;
        // Process newline characters
        else if (c == '\n' || c == '\r')
        {
            // Check if the response contains the specified header
            if (response.indexOf(rec_head) != -1)
            {
                // Analyze the range data
                range_analy(response);
            }
            else
            {
                // Print the response
                Serial.println(response);
            }

            // Clear the response string
            response = "";
        }
        // Append character to the response string
        else
            response += c;
    }
}

// Function to show logo on the display
void logoshow(void)
{
    // Clear the display
    display.clearDisplay();

    // Set text size and color
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);

    // Set cursor position and print text
    display.setCursor(0, 0);
    display.println(F("Get Range"));

    display.setCursor(0, 20);
    display.println(F("JSON"));
    display.setCursor(0, 40);
    display.println(F("A0"));

    // Display the content on the display
    display.display();

    // Delay for 2 seconds
    delay(2000);
}

// Function to analyze range data
void range_analy(String data)
{
    // Extract ID, range, and RSSI data from the response string
    String id_str = data.substring(data.indexOf("tid:") + 4, data.indexOf(",mask:"));
    String range_str = data.substring(data.indexOf("range:"), data.indexOf(",rssi:"));
    String rssi_str = data.substring(data.indexOf("rssi:"));

    // Arrays to store range and RSSI values
    int range_list[8];
    double rssi_list[8];
    int count = 0;

    // Parse range data
    count = sscanf(range_str.c_str(), "range:(%d,%d,%d,%d,%d,%d,%d,%d)",
                   &range_list[0], &range_list[1], &range_list[2], &range_list[3],
                   &range_list[4], &range_list[5], &range_list[6], &range_list[7]);

    // Check if the number of parsed values is correct
    if (count != 8)
    {
        Serial.println("RANGE ANALY ERROR");
        Serial.println(count);
        return;
    }

    // Parse RSSI data
    count = sscanf(rssi_str.c_str(), "rssi:(%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf)",
                   &rssi_list[0], &rssi_list[1], &rssi_list[2], &rssi_list[3],
                   &rssi_list[4], &rssi_list[5], &rssi_list[6], &rssi_list[7]);

    // Check if the number of parsed values is correct
    if (count != 8)
    {
        Serial.println("RSSI ANALY ERROR");
        Serial.println(count);
        return;
    }

    // Create JSON string
    String json_str = "";
    json_str = json_str + "{\"id\":" + id_str + ",";
    json_str = json_str + "\"range\":[";
    for (int i = 0; i < 8; i++)
    {
        if (i != 7)
            json_str = json_str + range_list[i] + ",";
        else
            json_str = json_str + range_list[i] + "]}";
    }

    // Print the JSON string
    Serial.println(json_str);
}