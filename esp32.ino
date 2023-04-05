#include <WiFi.h>
#include <ArduinoJson.h>
const char *ssid = "aryan";
const char *password = "12345678";
int IN1 = 23;
int IN2 = 22;
int IN3 = 1;
int IN4 = 3;
const int trigPin = 21;
const int echoPin = 19;

WiFiServer server(80);

int mytime_ud = 200;
int mytime_rl = 70;




#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;

float calculateDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED / 2;
  distanceInch = distanceCm * CM_TO_INCH;
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);

  return distanceCm;
}

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void left() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void right() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void forwardForTime(int time) {
  forward();    // Move forward
  delay(time);  // Wait for the specified time
  stop();       // Stop moving
}

void backwardForTime(int time) {
  backward();
  delay(time);
  stop();
}

void leftForTime(int time) {
  left();
  delay(time);
  stop();
}

void rightForTime(int time) {
  right();
  delay(time);
  stop();
}

void stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void avoidCollision() {
  float distance = calculateDistance();  // Get distance from obstacle

  // If the distance is less than 20 cm, stop and turn left
  if (distance < 20) {
    backwardForTime(500);
    int randNum = random(0, 2);  // Generate a random number between 0 and 1

    if (randNum == 0) {
      leftForTime(200);  // Turn left for 1 second
    } else {
      rightForTime(200);  // Turn right for 1 second
    }
    forward();
  }
}


bool pose = false;

void setup() {
  Serial.begin(115200);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(5, OUTPUT);  // set the LED pin mode
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);


  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
    if(pose == true)
        avoidCollision();

  WiFiClient client = server.available();  // listen for incoming clients

  if (client) {                     // if you get a client,
    Serial.println("New Client.");  // print a message out the serial port
    String currentLine = "";        // make a String to hold incoming data from the client



    while (client.connected()) {  // loop while the client's connected


      if (client.available()) {  // if there's bytes to read from the client,
        char c = client.read();  // read a byte, then
        Serial.write(c);         // print it out the serial monitor
        if (c == '\n') {         // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:

            client.print("<h1>Click <a href=\"/up\">up</a> .<br>");
            client.print("Click <a href=\"/down\">down</a> <br>");
            client.print("Click <a href=\"/right\">right</a>  <br>");
            client.print("Click <a href=\"/left\">left</a> <br>");
            client.print("Click <a href=\"/stop\">stop</a>  <br>");
            client.print("Click <a href=\"/ft\">forward time</a>  <br>");
            client.print("Click <a href=\"/bt\">backward time</a>  <br>");
            client.print("Click <a href=\"/rt\">right time</a>  <br>");
            client.print("Click <a href=\"/lt\">left time</a>  <br>");


            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {  // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
        
        // Check to see if the client request was "GET /H" or "GET /L":
        if (currentLine.endsWith("GET /up")) {
          forward();
        } else if (currentLine.endsWith("GET /down")) {
          backward();
        } else if (currentLine.endsWith("GET /left")) {
          left();
        } else if (currentLine.endsWith("GET /right")) {
          right();
        } else if (currentLine.endsWith("GET /stop")) {
          stop();
        } else if (currentLine.endsWith("GET /rt")) {
          rightForTime(mytime_rl);
        } else if (currentLine.endsWith("GET /lt")) {
          leftForTime(mytime_rl);
        } else if (currentLine.endsWith("GET /ft")) {
          forwardForTime(mytime_ud);
        } else if (currentLine.endsWith("GET /pose")) {
          if(pose == true ){
            pose = false;
          }
          else{
            pose = true;
          }
        }  else if (currentLine.endsWith("GET /bt")) {
          backwardForTime(mytime_ud);
          // }else if (currentLine.endsWith("GET /distance")) {
          //   float distance = calculateDistance();
          //   client.println("HTTP/1.1 200 OK");
          //   client.println("Content-Type: text/html");
          //   client.println();
          //   client.print("Distance (cm): ");
          //   client.println(distance);
          // }
        } else if (currentLine.endsWith("GET /distance")) {
            distanceCm = calculateDistance();
            client.print(distanceCm);
        }
      }
    }

    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
