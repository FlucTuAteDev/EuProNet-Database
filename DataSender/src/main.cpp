#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define BUTTON_COUNT 4 // Defines the number of buttons present
#define SWITCH 0x01

int okButtonPin = D2; // Pin of the ok button
int colorButtonPins[] = {D5, D6, D7, D8}; // Defines the button pins
int ledPins[] = {D0, D1, D3, D4};

// Network details
const char* SSID = "CiscoDiscoTracer";
const char* PASSWD = "homoknet";
const String APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"; // Api key, to check whether the connection is authorized

// Button press logic variables
enum State { None, Started, Discarded, Finished };
bool wasPressed[BUTTON_COUNT] = { false };
bool isPressed[BUTTON_COUNT] = { false };
State colorButtonStates[BUTTON_COUNT] = { State::None };
int currentPressedIndex = -1;

// HTTP connection variables
String httpServer = "http://192.168.43.17:5000/"; // FLASK implementation
String payload;
String httpResponseText;
int httpResponseCode;

// Serial communication variables
String serialResponseText = "";

// Helper functions
bool anyHasState()
{
    return std::any_of(std::begin(colorButtonStates), std::end(colorButtonStates), [](State n) { return n != State::None; });
}

// Send data through wifi
void SendData(int index)
{
    HTTPClient http; // Declares this device as an HTTP client
    http.begin(httpServer); // Begins the connection with the specified server
    http.addHeader("Content-Type", "application/x-www-form-0urlencoded"); // Defines the content type header
    // The values to be sent as a URL
    httpResponseText = 
        "apikey=" + APIKEYVALUE + 
        "&color=" + String((index + 1)) +
        "&state=" + String(colorButtonStates[index]);

    //Serial.println(httpResponseText);
    httpResponseCode = http.POST(httpResponseText); // Sends the request with method POST
    
    //Check if everything worked correctly    
    payload = http.getString();
    //Serial.println(httpResponseCode);
    //Serial.println(payload);
    http.end(); // Close the connection
}

void setup()
{
    Serial.begin(115200);
    // Connecting to wifi
    WiFi.begin(SSID, PASSWD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.print(".");
    }
    Serial.print("\nConnection established! IP address: ");
    Serial.print(WiFi.localIP());

    // Initialize buttons and leds
    for (int i = 0; i < BUTTON_COUNT; i++)
    {
        pinMode(colorButtonPins[i], INPUT);
        pinMode(ledPins[i], OUTPUT);
        digitalWrite(ledPins[i], LOW xor SWITCH);
    }

    pinMode(okButtonPin, INPUT);
}


void loop()
{
    // Goes through the color buttons available
    for (size_t i = 0; i < BUTTON_COUNT; i++)
    {
        isPressed[i] = digitalRead(colorButtonPins[i]) == HIGH;

        if (!isPressed[i] && wasPressed[i]) // If the button was pressed and then released
        {
            // If any of the buttons have a state and it's not this one then break 
            if (anyHasState() && colorButtonStates[i] == State::None)
            {
                wasPressed[i] = isPressed[i];
                break;
            }
            
            // If the pressed button had a started state change it to discarded
            if (colorButtonStates[i] == State::Started)
            {
                colorButtonStates[i] = State::Discarded;
                currentPressedIndex = -1;
                digitalWrite(ledPins[i], LOW xor SWITCH);
            }
            // If it didn't, set it to started
            else
            {
                colorButtonStates[i] = State::Started;
                currentPressedIndex = i;
                digitalWrite(ledPins[i], HIGH xor SWITCH);
            }

            SendData(i);
            // If the state was discarded reset it after sending the data
            if (colorButtonStates[i] == State::Discarded) colorButtonStates[i] = State::None;
        }
        wasPressed[i] = isPressed[i];
    }

    // If any of the buttons have a state and the ok button is pressed 
    if (anyHasState() && digitalRead(okButtonPin) == HIGH)
    {
        colorButtonStates[currentPressedIndex] = State::Finished;
        SendData(currentPressedIndex);
        colorButtonStates[currentPressedIndex] = State::None;
        digitalWrite(ledPins[currentPressedIndex], LOW xor SWITCH);
    }
    
    delay(10);
}