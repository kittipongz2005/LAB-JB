#include <WiFi.h>
#include <PubSubClient.h>

#define ANALOG_PIN 34  // กำหนดขา Analog ที่ต้องการอ่านค่า

const char* ssid = "SFRP_2.4GHz";
const char* password = "SFRP622568";
const char* mqtt_broker = "vf1b0d66.ala.dedicated.aws.emqxcloud.com";
const char* topic1 = "FIRSTNAME";
const char* topic2 = "LASTNAME";
const char* mqtt_username = "FILM";
const char* mqtt_password = "123456";
const int mqtt_port = 1883;
String client_id = "esp32-publisher-" + String(WiFi.macAddress());

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
    Serial.println("\nConnected to WiFi");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    client.setServer(mqtt_broker, mqtt_port);
    connectToBroker();
}

void connectToBroker() {
    while (!client.connected()) {
        Serial.println("Connecting to MQTT broker...");
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
        } else {
            Serial.print("Failed to connect, state: ");
            Serial.println(client.state());
            delay(5000);
        }
    }
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi disconnected, reconnecting...");
        WiFi.begin(ssid, password);
        delay(5000);
        return;
    }
    if (!client.connected()) {
        connectToBroker();
    }
    client.loop();

    int sensorValue = analogRead(ANALOG_PIN);  // อ่านค่าจากเซ็นเซอร์
    String payload1 = "KITTIPONG ";
    String payload2 = "WONGJINDA";

    Serial.println("Publishing to DEPARTMENT...");
    client.publish(topic1, payload1.c_str(), true);  // QoS 1

    Serial.println("Publishing to NAME...");
    client.publish(topic2, payload2.c_str(), true);  // QoS 1

    delay(5000);  // ส่งข้อมูลทุก 5 วินาที
}