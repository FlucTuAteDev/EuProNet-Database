#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define COLOR_COUNT 4 // Defines the number of color buttons present
// Switch high / low for leds
#define SWITCH 0x01

// Pins
int finishButtonPin = D3;
int colorButtonPins[] = {D5, D6, D7, D8};
int ledPins[] = {D0, D1, D2, D4};

// Button press logic variables
enum State { None, Started, Discarded, Finished };
State colorButtonStates[COLOR_COUNT] { None };
volatile bool stateChanged = false;
volatile int stateChIndex = -1;

// Network details
const char* SSID = "SandroPC";
const char* PASSWD = "123456789";
const String APIKEY = "wV9ysymCPn9yTYcilpIT"; // Api key, to check whether the connection is authorized

// HTTP connection variables
String httpServer = "http://192.168.137.208:5000/"; // FLASK implementation
String payload;
String httpResponseText;
int httpResponseCode;

// Send data through wifi
void SendData(int color, int state)
{
    HTTPClient http; // Declares this device as an HTTP client
    http.begin(httpServer); // Begins the connection with the specified server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); // Defines the content type header
    // The values to be sent as a URL
    httpResponseText = 
        "apikey=" + APIKEY + 
        "&color=" + String(color) + 
        "&state=" + String(state);

    Serial.println(httpResponseText);
    httpResponseCode = http.POST(httpResponseText); // Sends the request with method POST
    
    //Check if everything worked correctly    
    payload = http.getString();
    Serial.println(httpResponseCode);
    //Serial.println(payload);
    http.end(); // Close the connection
}

// Runs when a color button is pressed
void ICACHE_RAM_ATTR colorInterrupt(void* pinp)
{
    // If the previous interrupt wasn't processed then don't proceed
    if (stateChanged) return;

    // Get the GPIO pin from the pointer
    int pin = *(int*)pinp;

    // If there is a button with some state which is not the currently pressed one then don't proceed
    for (int i = 0; i < COLOR_COUNT; i++)
    {
        if (colorButtonPins[i] != pin && colorButtonStates[i] != State::None)
            return;
    }

    // Search for the current button in the pins array
    for (int i = 0; i < COLOR_COUNT; i++)
    {
        if (colorButtonPins[i] == pin)
        {
            // If the button doesn't have a state then set it to started and turn on the indicator led
            if (colorButtonStates[i] == State::None)
            {
                colorButtonStates[i] = State::Started;
                digitalWrite(ledPins[i], HIGH xor SWITCH);
            }
            // If its state is started then set it to discarded and turn off the indicator led
            else if (colorButtonStates[i] == State::Started)
            {
                colorButtonStates[i] = State::Discarded;
                digitalWrite(ledPins[i], LOW xor SWITCH);
            }
            stateChanged = true;
            stateChIndex = i;
            break;
        }
    }
}

// Runs when the finish button is pressed
void ICACHE_RAM_ATTR finishInterrupt()
{
    // If the previous interrupt wasn't processed then don't proceed
    if (stateChanged) return;

    // Search for the pin with a started state
    for (int i = 0; i < COLOR_COUNT; i++)
    {
        if (colorButtonStates[i] == State::Started)
        {
            // Set its state to finished and turn off the indicator led
            colorButtonStates[i] = State::Finished;
            stateChanged = true;
            stateChIndex = i;
            digitalWrite(ledPins[i], LOW xor SWITCH);
        }
    }
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
    Serial.println(WiFi.localIP());

    // Initialize buttons and leds
    for (int i = 0; i < COLOR_COUNT; i++)
    {
        pinMode(ledPins[i], OUTPUT);
        digitalWrite(ledPins[i], LOW xor SWITCH);
        pinMode(colorButtonPins[i], INPUT);
        attachInterruptArg(digitalPinToInterrupt(colorButtonPins[i]), colorInterrupt, &colorButtonPins[i], RISING);
    }

    pinMode(finishButtonPin, INPUT);
    attachInterrupt(digitalPinToInterrupt(finishButtonPin), finishInterrupt, RISING);
}

void loop()
{
    if (stateChanged)
    {
        SendData(stateChIndex + 1, colorButtonStates[stateChIndex]);
        if (colorButtonStates[stateChIndex] != State::Started)
            colorButtonStates[stateChIndex] = State::None;
        stateChanged = false;
        stateChIndex = -1;
    }
}
