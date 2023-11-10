#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <Arduino_JSON.h>

#define DHTPIN 2  
#define DHTTYPE DHT22

#define LEDPIN 5

#define BOARDID "1"

const char* ssid = "Minato Aqua";
const char* password = "2914328376";


DHT dht(DHTPIN,DHTTYPE);


const String serverName = "https://withchaz.pythonanywhere.com";


unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

void setup() {
  Serial.begin(9600); 
  dht.begin();

  pinMode(LEDPIN,OUTPUT);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

    float h = dht.readHumidity();
    float t = dht.readTemperature();
      


      char s[200] ;
      sprintf(s, "/?id=%s&hum=%.2f&temp=%.2f",BOARDID,h,t);
      String serverPath = serverName + s;
      
      http.begin(serverPath);
      // Send HTTP GET request
      int httpResponseCode = http.GET();
      
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String serverPayload = http.getString();
        Serial.println(serverPayload);
        const char* s = serverPayload.c_str();
        digitalWrite(LEDPIN,!strcmp(s,"True"));
    }


      
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
 

