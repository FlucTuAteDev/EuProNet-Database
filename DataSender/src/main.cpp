#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define BUTTON_COUNT 4 // Defines the number of color buttons present

int okButtonPin = D2; // Pin of the ok button
int colorButtonPins[] = {D8, D7, D6, D5}; // Defines the color button pins

// Network details
const char* SSID = "GucziFamily";
const char* PASSWD = "Spiderma-6";
const String APIKEY = "wV9ysymCPn9yTYcilpIT"; // Api key, to check whether the connection is authorized

// Button press logic variables
bool wasPressed[] = {false, false, false, false};
bool isPressed[] = {false, false, false, false};
bool currentButtonState = false;
bool colorButtonStates[] = {false, false, false, false};
String colorButtonColors[] = {"Red", "Yellow", "Green", "Blue"};
bool okButtonState = false;
bool discarded = false;
String state;
int currentButton = -1; // -1 -> No button selected

// HTTP connection variables
String httpServer = "http://192.168.1.2:5000/"; // FLASK implementation
String payload;
String httpResponseText;
int httpResponseCode;

// Serial communication variables
String serialResponseText = "";

// Helper functions
int getIntFromBool(bool array[], int arrayLength)
{
    for (size_t i = 0; i < arrayLength; i++)
    {
        if (array[i])
            return i + 1;
    }
    return -1;
}

void resetBoolArray(bool array[], int arrayLength)
{
    for (size_t i = 0; i < arrayLength; i++)
    {
        array[i] = false;
    }
}

// Send data through wifi
void SendDataWifi()
{
    HTTPClient http; // Declares this device as an HTTP client
    http.begin(httpServer); // Begins the connection with the specified server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); // Defines the content type header

    // The values to be sent as a URL
    httpResponseText = 
        "apikey=" + APIKEY +
        "&color=" + String(getIntFromBool(colorButtonStates, BUTTON_COUNT)) +
        "&state=" + String(discarded ? "2" : (okButtonState ? "3" : "1"));

    Serial.println(httpResponseText);
    httpResponseCode = http.POST(httpResponseText); // Sends the request with method POST
    
    //Check if everything worked correctly    
    payload = http.getString();
    Serial.println(httpResponseCode);
    Serial.println(payload);

    http.end(); // Close the connection

    if (okButtonState) // If the ok button was pressed than reset the presses
    {
        resetBoolArray(colorButtonStates, BUTTON_COUNT);
        currentButton = -1;
    }
}

// Send data through serial communication
/*
void SendDataSerial()
{
    serialResponseText = 
        "apikey:" + APIKEY +
        ";color:" + String(getIntFromBool(colorButtonStates, BUTTON_COUNT)) +
        ";state:" + String(discarded ? "2" : (okButtonState ? "3" : "1"));
    
    Serial.println(serialResponseText);
}
*/

void setup()
{
    Serial.begin(115200);

    // Connecting to home wifi
    WiFi.begin(SSID, PASSWD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.print(".");
    }

    Serial.print("\nConnection established! IP address: ");
    Serial.println(WiFi.localIP());

    // Button init
    for (int button : colorButtonPins)
    {
        pinMode(button, INPUT);
    }
    pinMode(okButtonPin, INPUT);
}

void loop()
{
    if (WiFi.status() == WL_CONNECTED) // Only do anything if we are connected to a network
    {
        // Goes through the color buttons available
        for (size_t i = 0; i < BUTTON_COUNT; i++)
        {
            currentButtonState = digitalRead(colorButtonPins[i]) == HIGH ? true : false; // Stores the current button's state
            isPressed[i] = currentButtonState; // Whether the button is pressed now
            if (!isPressed[i] && wasPressed[i]) // The user lets the button go
            {
                if (currentButton != -1 && !colorButtonStates[i]) // If a color is selected at the moment and it is not this button, don't process the request
                {
                    wasPressed[i] = currentButtonState;
                    break;
                }
                else if (currentButton != -1 && colorButtonStates[i]) // If it is this button than discard
                {
                    discarded = true;
                }
                currentButton = discarded ? -1 : i; // Set the current button's value to i if it is not discarded
                if (!discarded)
                {
                    colorButtonStates[i] = !colorButtonStates[i]; // Negate the button's state
                }
                SendDataWifi(); // Send the data to the server
                if (discarded)
                {
                    discarded = false;
                    colorButtonStates[i] = !colorButtonStates[i]; // Negate the button's state
                }
            }
            wasPressed[i] = currentButtonState; // Stores the button press of the cycle
        }

        okButtonState = currentButton != -1 && digitalRead(okButtonPin) == HIGH; // The ok button should only be pressed if there is already a color button pressed
        if (okButtonState) // If that's the case then send the data
            SendDataWifi();
    }
}