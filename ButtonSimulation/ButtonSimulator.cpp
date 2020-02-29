#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#define BUTTON_COUNT 4

// Initiaizing variables
int buttons[] = {D8, D7, D6, D5};
int buttonState;
const char* SSID = "GucziFamily";
const char* PASSWD = "PASSWORD";
const String APIKEYVALUE = "wV9ysymCPn9yTYcilpIT";
bool wasPressed[] = {false, false, false, false};
bool isPressed[] = {false, false, false, false};
bool hasOne = false;
char resultPresses[4];

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

HTTPClient http;
void loop()
{
    if (WiFi.status() == WL_CONNECTED)
    {
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
        if (hasOne)
        {
            http.begin("192.168.1.2/ButtonListener/index.php");
            http.addHeader("Content-Type", "application/x-www-form-urlencoded");
            String httpResponseText = "apiKey=" + APIKEYVALUE + "&time=" + String(time(0)) +"&buttons=" + String(resultPresses);
            Serial.println(httpResponseText);
            int httpResponseCode = http.POST(httpResponseText);
            if (httpResponseCode > 0)
                Serial.println("Data was sent successfully!");
            else
                Serial.println("ERROR: " + String(httpResponseCode));

            http.end();
            hasOne = false;
        }
    }
}