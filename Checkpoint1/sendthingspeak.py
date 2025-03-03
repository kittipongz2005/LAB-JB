//-- ทดสอบส่งข้อมูลขึ้น ThinkSpeak

#include <WiFi.h>
#include "ThingSpeak.h"  // Always include ThingSpeak after other headers

WiFiClient client;

const int LED = 32;  // GPIO สำหรับ LED
const int SENSOR_PIN = 34;  // ขา ADC สำหรับอ่านค่าจากเซ็นเซอร์ (ESP32 ใช้ ADC1)

// ตั้งค่า WiFi
const char *ssid = "SFRP_2.4GHz";      // ใส่ชื่อ WiFi ของคุณ
const char *password = "SFRP622568";  // ใส่รหัสผ่าน WiFi ของคุณ

// ตั้งค่า ThingSpeak
unsigned long myChannelNumber = 2862155;  // ใส่หมายเลข Channel
const char *myWriteAPIKey = "IZ0IAKMRP61LNRX1";  // ใส่ API Key ของคุณ

void setup() {
  Serial.begin(115200);  // เปิด Serial Monitor
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);  // เปิด LED เพื่อแสดงว่ากำลังเชื่อมต่อ WiFi

  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);  // เริ่มต้นใช้งาน ThingSpeak
  
  // เชื่อมต่อ WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected...");
    delay(500);
  }
  
  digitalWrite(LED, LOW);  // ปิด LED เมื่อเชื่อมต่อสำเร็จ
  Serial.println("WiFi Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(LED, !digitalRead(LED));  // กระพริบ LED แสดงสถานะการส่งข้อมูล

    int sensorValue = analogRead(SENSOR_PIN);  // อ่านค่าจากเซ็นเซอร์ (ADC)
    int hallSensorValue = hallRead();  // อ่านค่าจาก Hall Effect Sensor ใน ESP32

    ThingSpeak.setField(1, sensorValue);
    ThingSpeak.setField(2, hallSensorValue);

    int response = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
    if (response == 200) {
      Serial.println("Channel update successful.");
    } else {
      Serial.println("Problem updating channel. HTTP error code " + String(response));
    }
  } else {
    digitalWrite(LED, HIGH);  // เปิด LED ค้างถ้า WiFi หลุด
  }
  
  delay(15000);  // หน่วงเวลา 15 วินาที ก่อนส่งข้อมูลรอบถัดไป
}