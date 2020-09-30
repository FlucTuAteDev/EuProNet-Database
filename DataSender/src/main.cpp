#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define BUTTON_COUNT 4 // Defines the number of buttons present
#define SWITCH 0x01

int okButtonPin = D2; // Pin of the ok button
int colorButtonPins[] = {D5, D6, D7, D8}; // Defines the button pins
int ledPins[] = {D0, D1, D3, D4};

// Network details
const char* SSID = "GucziFamily";
const char* PASSWD = "Spiderma-6";
const String APIKEYVALUE = "wV9ysymCPn9yTYcilpIT"; // Api key, to check whether the connection is authorized

// Button press logic variables
enum State { None, Started, Discarded, Finished };
bool wasPressed[BUTTON_COUNT] = { false };
bool isPressed[BUTTON_COUNT] = { false };
State colorButtonStates[BUTTON_COUNT] = { State::None };

// HTTP connection variables
String httpServer = "http://192.168.1.112:5000/"; // FLASK implementation
String payload;
String httpResponseText;
int httpResponseCode;

// Serial communication variables
String serialResponseText = "";

// Helper functions

// Send data through wifi
void SendData(int index)
{
    HTTPClient http; // Declares this device as an HTTP client
    http.begin(httpServer); // Begins the connection with the specified server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); // Defines the content type header
    // The values to be sent as a URL
    httpResponseText = 
        "apikey=" + APIKEYVALUE + 
        "&color=" + String((index + 1)) +
        "&state=" + String(colorButtonStates[index]);

    Serial.println(httpResponseText);
    httpResponseCode = http.POST(httpResponseText); // Sends the request with method POST
    
    //Check if everything worked correctly    
    payload = http.getString();
    Serial.println(httpResponseCode);
    //Serial.println(payload);
    http.end(); // Close the connection
}

// Runs when a color button is pressed
// void ICACHE_RAM_ATTR colorInterrupt(void* pinp)
// {
//     // If the previous interrupt wasn't processed then don't proceed
//     if (stateChanged) return;

//     // Get the GPIO pin from the pointer
//     int pin = *(int*)pinp;

//     // If there is a button with some state which is not the currently pressed one then don't proceed
//     for (int i = 0; i < COLOR_COUNT; i++)
//     {
//         if (colorButtonPins[i] != pin && colorButtonStates[i] != State::None)
//             return;
//     }

//     // Search for the current button in the pins array
//     for (int i = 0; i < COLOR_COUNT; i++)
//     {
//         if (colorButtonPins[i] == pin)
//         {
//             // If the button doesn't have a state then set it to started and turn on the indicator led
//             if (colorButtonStates[i] == State::None)
//             {
//                 colorButtonStates[i] = State::Started;
//                 digitalWrite(ledPins[i], HIGH xor SWITCH);
//             }
//             // If its state is started then set it to discarded and turn off the indicator led
//             else if (colorButtonStates[i] == State::Started)
//             {
//                 colorButtonStates[i] = State::Discarded;
//                 digitalWrite(ledPins[i], LOW xor SWITCH);
//             }
//             stateChanged = true;
//             stateChIndex = i;
//             break;
//         }
//     }
// }

// // Send data through serial communication
// void SendDataSerial()
// {
//     serialResponseText = 
//         "apiKey=" + APIKEYVALUE + 
//         "&buttons=" + getStringFromBool(colorButtonStates, BUTTON_COUNT) +
//         "&discarded=" + getStringFromBool(discarded) +
//         "&finished=" + getStringFromBool(okButtonState);
    
//     Serial.println(serialResponseText);
// }

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

bool anyHasState(State array[])
{
    return std::any_of(std::begin(colorButtonStates), std::end(colorButtonStates), [](State n) { return n != State::None; });
}

int currentPressedIndex = -1;
void loop()
{
    // Goes through the color buttons available
    for (size_t i = 0; i < BUTTON_COUNT; i++)
    {
        isPressed[i] = digitalRead(colorButtonPins[i]) == HIGH;
        //Serial.println(isPressed[i]);

        if (!isPressed[i] && wasPressed[i]) // If the button was pressed and then released
        {
            // If any of the buttons have a state and it's not this one then break 
            if (anyHasState(colorButtonStates) && colorButtonStates[i] == State::None)
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
            // If it didn't set it to started
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
    if (anyHasState(colorButtonStates) && digitalRead(okButtonPin) == HIGH)
    {
        // if (currentPressedIndex == -1) return;
        colorButtonStates[currentPressedIndex] = State::Finished;
        SendData(currentPressedIndex);
        colorButtonStates[currentPressedIndex] = State::None;
        digitalWrite(ledPins[currentPressedIndex], LOW xor SWITCH);
        // for (int led : ledPins) digitalWrite(led, LOW xor SWITCH);
    }
    
    delay(10);
}
