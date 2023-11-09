#include <WiFi.h>
#include <DHT.h>

#define LEDPINN 5

#define DHTPIN 2
#define DHTTYPE DHT22

#define BOARD_ID "1"

const char* ssid = "Minato Aqua";
const char* password = "2914328376";

const char* serverName = "Withchaz.pythonanywhere.com";


DHT dht(DHTPIN,DHTTYPE);

WiFiClient client;

void setup() {
  Serial.begin(9600);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
  
  
}




void loop() {
  if (client.connect(serverName,80)){
    Serial.println("Connected");
  }
  else {
    Serial.println("Disconnected");
  }

  char buf[200];
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  sprintf(buf,"GET /?id=%s&hum=%.2f&temp=%.2f HTTP/1.1",BOARD_ID,h,t);
  

  client.println(buf);
  client.printf("Host: %s\n",serverName);
  client.println("Connection: close");
  client.println(); // end HTTP request header

  
  while (client.connected()) {
    while (client.available()) {
      String line = client.readStringUntil('\n');
      
      Serial.println(line);
    }
  }
  client.flush();
}
