#include <WiFi.h>
#include <PubSubClient.h>

//DHT11
#include "DHT.h"
#define DHT_PIN 15     
#define DHT_TYPE DHT11 
DHT dhtt(DHT_PIN, DHT_TYPE);

// Update these with values suitable for your network.
const char* ssid = "dimz";
const char* password = "qwertyuiop";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
String modifiedHostname;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);

  // Retrieve MAC address
  uint8_t mac[6];
  WiFi.macAddress(mac);

  // Format MAC address as string
  char macString[18];
  sprintf(macString, "%02X%02X%02X%02X%02X%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  // Get original hostname
  String originalHostname = "ESP32suhu";

  // Append MAC address to the hostname
  modifiedHostname = originalHostname + "_" + macString;

  // Set the modified hostname
  WiFi.setHostname(modifiedHostname.c_str());
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe("/esp32/mqtt/in");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  dhtt.begin();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
  //dht11
  //float h = dhtt.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dhtt.readTemperature();
  Serial.println(t);

      // Convert the value to a char array
    char tempString[8];
    dtostrf(t, 1, 2, tempString);
    Serial.print("Temperature: ");
    Serial.println(tempString);
    Serial.println(modifiedHostname);
//    client.publish("/esp32-mqtt/temp", tempString); 

    // Publish data to MQTT topic
    char payload[50];
    sprintf(payload, "{\"id\":\"%s\",\"temperature\":%2.f}", modifiedHostname.c_str(), t);
    Serial.println(payload);
    client.publish("/esp32-mqtt/temp", payload);
  }
}
