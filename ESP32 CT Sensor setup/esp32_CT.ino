#include "EmonLib.h"      //Energy monitoring library
#include <WiFi.h>
#include <esp_sleep.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include <HTTPClient.h>
#define uS_TO_S_FACTOR 1000000  
#define TIME_TO_SLEEP  10           // seconds to sleep

const char* ssid     = "Loading...";          //wifi ssid 
const char* password = "098765432";          //wifi password
// REPLACE with your Domain name and URL path or IP address with path
const char* serverName = "http://18.116.3.198/post-esp-data.php";              //aws ip
//const char* serverName = "http://192.168.80.142/post-esp-data.php";          // local ip if used local server
// Keep this API Key value to be compatible with the PHP code provided in the project page. 
// If you change the apiKeyValue value, the PHP file /post-data.php also needs to have the same key 
String apiKeyValue = "tPmAT5Ab7F2"; // 


EnergyMonitor emon1;
void setup() {
  // put your setup code here, to run once:
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);                //disable brownout detector
Serial.begin(115200);
pinMode(LED_BUILTIN, OUTPUT);
emon1.current(34,60.6);


 esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);      //setup sleep timer
}

void loop() {
  // put your main code here, to run repeatedly:
double wh;                                  // initialise variables
wh=0;
double Irms;
double power;
float temp1;
  for (int i = 0; i <= 5; i++)                    //loop for 6 times i.e 1 minuite
  {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("woke ");
    Irms = (emon1.calcIrms(1480)/8);
    Irms = (emon1.calcIrms(1480)/8);
    Irms = (emon1.calcIrms(1480)/8);
    Irms = (emon1.calcIrms(1480)/8);
    Irms = (emon1.calcIrms(1480)/8);              //get current reading from sensor

Serial.print("irms=");
    Serial.println(Irms);
    power = Irms * 230;
    Serial.print("power=");
    Serial.println(power);
    temp1 = Irms * 230 * 0.00278;               //calculate Wh
        Serial.print("temp1=");
    Serial.println(temp1);
wh = wh+temp1;                                    // add reading to previous value
    Serial.println(wh);
    Serial.println("now sleeping: ");
    digitalWrite(LED_BUILTIN, LOW);
   
    esp_light_sleep_start();                        //esp goes to light sleep
    
  }

  WiFi.begin(ssid, password);                                 // start wifi
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    Serial.print(".");
    digitalWrite(LED_BUILTIN, LOW);
  }
    Serial.println("WiFi connected");                     // inform that wifi is connected
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    
    // Your Domain name with URL path or IP address with path
    http.begin(serverName);
    
    // Specify content-type header
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
    // Prepare your HTTP POST request data
    String httpRequestData = "api_key=" + apiKeyValue + "&value2=" + String(wh)+ "";       // sends value to mysql server
    Serial.print("httpRequestData: ");
    Serial.println(httpRequestData);

    // Send HTTP POST request
    int httpResponseCode = http.POST(httpRequestData);                 //get error code if failed
         
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
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
ESP.restart();                      // restart after every successful request made to cloud
}
