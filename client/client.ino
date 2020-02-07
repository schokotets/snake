#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

char *ssid = "snake"; // network SSID (name)
char *pass = "n3tw0rk!"; // network password
unsigned int udpPort = 9900; // local port to listen for UDP packets

const int buttonLeft = 16;
const int buttonRight = 5;

const int8_t ID = 0;

// A UDP instance to let us send and receive packets over UDP
WiFiUDP udp;
IPAddress broadcastIP;

void setup() {
  Serial.begin(38400);

  pinMode(buttonLeft, INPUT);
  pinMode(buttonRight, INPUT);
  
  WiFi.begin(ssid, pass);
  
  while ( WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  
  Serial.println("[setup] WiFi connected");
  Serial.print("[setup] IP address: ");
  Serial.println(WiFi.localIP());
  
  udp.begin(udpPort);
  
  broadcastIP = WiFi.localIP();
  broadcastIP[3] = 255;
  Serial.print("[setup] Broadcast IP: ");
  Serial.println(broadcastIP);
}

float rad = 0;
void loop() {
  if(digitalRead(buttonLeft) == HIGH) {
    rad+=0.1;
    Serial.println("Turning left");
  }
  if(digitalRead(buttonRight) == HIGH) {
    rad-=0.1;
    Serial.println("Turning right");
  }
  if(rad < -2*PI)
    rad += 2*PI;
  if(rad > 2*PI)
    rad -= 2*PI;
  int8_t x = cos(rad)*128;
  int8_t y = sin(rad)*128;
  
  Serial.print("ID: ");
  Serial.print(ID);
  Serial.print(" rad: ");
  Serial.print(rad);
  Serial.print(" x: ");
  Serial.print(x);
  Serial.print(" y: ");
  Serial.println(y);

  udp.beginPacket(broadcastIP, udpPort);
  byte message[3];
  message[0]=ID;
  message[1]=x;
  message[2]=y;
  udp.write(message, 3);
  udp.endPacket();
  
  delay(100);
}
