//-- ทดสอบอ่านค่ากลับมาจาก Think speak แสดงผ่าน Serial port


#include <WiFi.h>
#include <ThingSpeak.h>

// กำหนดข้อมูล Wi-Fi
const char* ssid = "SFRP_2.4GHz";          // ชื่อ Wi-Fi ของคุณ
const char* password = "SFRP622568";       // รหัสผ่าน Wi-Fi ของคุณ

// กำหนด API Key ของ ThingSpeak
unsigned long myChannelNumber = 2862155;   // Channel ID ของคุณ
const char* myAPIKey = "2C2H8VFRWPVOC8CK"; // Read API Key ของคุณ

WiFiClient client;

void setup() {
  // เริ่มต้นการเชื่อมต่อ Serial
  Serial.begin(115200);
  
  // เชื่อมต่อกับ Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.print("Connecting to WiFi");
  
  // รอจนกว่าเชื่อมต่อ Wi-Fi ได้
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // แสดงข้อความเมื่อเชื่อมต่อ Wi-Fi สำเร็จ
  Serial.println("");
  Serial.print("Connected to WiFi");
  Serial.println(WiFi.localIP());
  
  // เชื่อมต่อกับ ThingSpeak
  ThingSpeak.begin(client);
}

void loop() {
  // อ่านข้อมูลจาก ThingSpeak (Field 2) และแสดงข้อมูลเก่า
  int numberOfPoints = 10;  // จำนวนจุดข้อมูลที่ต้องการดึงจาก ThingSpeak (ไม่เกิน 800)
  
  for (int i = 0; i < numberOfPoints; i++) {
    // ดึงข้อมูลจาก ThingSpeak โดยใช้ API Key ที่ถูกต้อง
    float hallData = ThingSpeak.readFloatField(myChannelNumber, 2, myAPIKey); // ใช้ myAPIKey แทน i
    
    if (hallData != NAN) {
      // แสดงข้อมูลผ่าน Serial Monitor
      Serial.print("Hall Data at index ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(hallData);
    } else {
      Serial.print("Failed to retrieve data at index ");
      Serial.println(i);
    }
  }

  // รอ 20 วินาทีเพื่อไม่ให้คำขอซ้ำบ่อยเกินไป
  delay(20000); 
}