#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define BUTTON_COUNT 4 // Defines the number of buttons present

int buttons[] = {D8, D7, D6, D5}; // Defines the button pins
int buttonState;

// Network details
const char* SSID = "GucziFamily";
const char* PASSWD = "Spiderma-6";

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
    Serial.print(WiFi.localIP());

    // Button init
    for (int button : buttons)
    {
        pinMode(button, INPUT);
    }
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);

}

const String APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"; // Api key, to check whether the connection is authorized

// Button press logic variables
bool wasPressed[] = {false, false, false, false};
bool isPressed[] = {false, false, false, false};
bool hasOne = false;

String resultPresses = "0000"; // The string that is going to be sent

// HTTP connection variables
String httpServer = "http://192.168.1.2/ButtonListener/";

// HTTP response check
String payload;
String httpResponseText;
int httpResponseCode;

void loop()
{
    if (WiFi.status() == WL_CONNECTED) // Only do anything if we are connected to a network
    {
        // Checks whether a button was pressed
        for (size_t i = 0; i < BUTTON_COUNT; i++)
        {
            isPressed[i] = digitalRead(buttons[i]) == HIGH ? true : false;
            if (!isPressed[i] && wasPressed[i])
            {
                resultPresses[i] = '1';
                hasOne = true;
            }
            else
            {
                resultPresses[i] = '0';
            }
            wasPressed[i] = digitalRead(buttons[i]) == HIGH ? true : false;
        }
        if (hasOne) // If a button was pressed
        {
            HTTPClient http; // Declares this device as an HTTP client
            http.begin(httpServer); // Begins the connection with the specified server
            http.addHeader("Content-Type", "application/x-www-form-urlencoded"); // Defines the content type header
            // The values to be sent as a URL
            httpResponseText = 
                "apiKey=" + APIKEYVALUE + 
                "&time=" + String(time(0)) + 
                "&buttons=" + resultPresses;

            //Serial.println(httpResponseText);

            httpResponseCode = http.POST(httpResponseText); // Sends the request with method POST
            
            //Check if everything worked correctly    
            payload = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(payload);

            http.end(); // Close the connection

            hasOne = false;
        }
    }
}