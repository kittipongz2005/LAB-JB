#include <WiFi.h>
#include <PubSubClient.h>

#define BUILTIN_LED 32
#define ANALOG_PIN 34  // กำหนดขา Analog ที่จะอ่านค่าข้อมูล

const char* ssid = "SFRP_2.4GHz";
const char* password = "SFRP622568";
const char* mqtt_broker = "vf1b0d66.ala.dedicated.aws.emqxcloud.com";
const char* topic = "TEST";
const char* mqtt_username = "FILM";
const char* mqtt_password = "123456";
const int mqtt_port = 1883;
String client_id = "esp32-client-";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println("\nWiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    
    while (!client.connected()) {
        client_id += String(WiFi.macAddress());
        Serial.printf("Connecting to MQTT Broker as %s\n", client_id.c_str());
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT Broker");
        } else {
            Serial.print("Failed, rc=");
            Serial.println(client.state());
            delay(2000);
        }
    }
    client.subscribe(topic, 1);  // Subscribe ด้วย QoS 1
}

void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received in topic: ");
    Serial.println(topic);
    Serial.print("Message: ");
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println("\n-----------------------");
}

void loop() {
    client.loop();
    int analogValue = analogRead(ANALOG_PIN);  // อ่านค่าจากขา Analog
    char message[10];
    sprintf(message, "%d", analogValue);
    Serial.print("Publishing analog value: ");
    Serial.println(message);
    
    // ส่งข้อมูลไปยัง MQTT Broker ด้วย QoS 1
    if (client.publish(topic, message, true)) {
        Serial.println("Message sent successfully");
    } else {
        Serial.println("Message failed to send");
    }
    delay(5000);
}