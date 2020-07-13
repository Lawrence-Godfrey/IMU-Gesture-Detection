#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#include <xCore.h>
#include <xSI01.h>

xSI01 SI01;
HTTPClient http;

char* ssid = "<SSID>";
char* password = "<PSK>";

const int num_samples = 150;

String getSample() {
  SI01.poll();

  return  "\"" + String(SI01.getGX())    + "\"" +"," + "\"" + String(SI01.getGY())  + "\"" + "," + "\"" + String(SI01.getGZ())  + "\"" + "," + 
          "\"" + String(SI01.getAX())    + "\"" +"," + "\"" + String(SI01.getAY())  + "\"" + "," + "\"" + String(SI01.getAZ())  + "\"" + "," + 
          "\"" + String(SI01.getMX())    + "\"" +"," + "\"" + String(SI01.getMY())  + "\"" + "," + "\"" + String(SI01.getMZ())  + "\"";
}

String getAllSamples() {
  String data = "";

  unsigned long lastPrint = 0;
  int i = 0;

  while(i < num_samples) {
    if(lastPrint + 10 < millis()) {
      data += getSample() + "\r\n";  
      
      delay(0);
      lastPrint = millis();
      i++;
    }
  }

  return data;
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  delay(10);
  
  if (!SI01.begin()) {
    Serial.println("Failed to communicate with SI01.");
    Serial.println("Check the Connector");
  } else {
    Serial.println("Connected to SI01");
  }

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Beggining http");
}

void loop() {
  http.begin("http://<ip address>:8080/");

  http.addHeader("Content-Type", "text/plain");

   if (Serial.available() > 0) {


    Serial.println("Press Enter to Start");
    String data = getAllSamples();    
    Serial.println("Stop");

    int httpCode = http.POST(data);

    if(!(httpCode < 0)) {
      Serial.print("http code: ");
      Serial.println(httpCode);
    }

    http.end();
    while(Serial.read() >= 0);  // clear serial input buffer
  }
}
