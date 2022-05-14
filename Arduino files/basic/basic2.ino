#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <WiFiClient.h>
const char *ssid =  "Darshansh";     // replace with your wifi ssid and wpa2 key
const char *pass =  "dhruvsh111";

const int duration = 500;

#define sjmotorin1 D6
#define sjmotorin2 D7
#define sjmotorenable D8

int sjmotspeed=120;

WiFiServer server(80);

void setup() 
{
       Serial.begin(9600);
       
       pinMode(sjmotorin1,OUTPUT);
       pinMode(sjmotorin2,OUTPUT);
       pinMode(sjmotorenable,OUTPUT);
  
       delay(10);
               
       Serial.println("Connecting to ");
       Serial.println(ssid); 
 
       WiFi.begin(ssid, pass); 
       while (WiFi.status() != WL_CONNECTED) 
          {
            delay(500);
            Serial.print(".");
          }
      Serial.println("");
      Serial.println("WiFi connected"); 

      Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();

}
int value=0; 
void loop() {
  
  WiFiClient client = server.available();   // listen for incoming clients

  if (client) {                             // if you get a client,
    //Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            
            client.print("<a href=\"/UP\">UP</a>.<br>");
            client.print("<a href=\"/DOWN\">DOWN</a>.<br>");

            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        if (currentLine.endsWith("GET /UP")) {
          //FOR UP
          analogWrite(sjmotorenable,0);
          digitalWrite(sjmotorin1, HIGH);
          digitalWrite(sjmotorin2, LOW);
          delay(duration/5);
          digitalWrite(sjmotorin1, LOW);
          digitalWrite(sjmotorin2, LOW);
        }
             if (currentLine.endsWith("GET /DOWN")) {
          //FOR DOWN
          analogWrite(sjmotorenable,0);
          digitalWrite(sjmotorin1, LOW);
          digitalWrite(sjmotorin2,HIGH);
          delay(duration/5);
          digitalWrite(sjmotorin1, LOW);
          digitalWrite(sjmotorin2, LOW);
        }
      }
    }
    // close the connection:
    client.stop();
    //Serial.println("Client Disconnected.");
  }
}
