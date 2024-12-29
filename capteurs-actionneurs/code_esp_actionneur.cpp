//tutoriel suivi: https://randomnerdtutorials.com/esp8266-nodemcu-http-get-post-arduino/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "Grove_Temperature_And_Humidity_Sensor.h" //librairie pour utiliser le capteur


// Préciser de quel dht il s'agit et sur quel pin
#define DHTTYPE DHT11
#define DHTPIN 0
DHT dht(DHTPIN, DHTTYPE);

// Connection au réseau WiFi
const char* ssid = "Redmi Note 12 Pro";
const char* password = "spaghetti";
//adresse IPv4 de la carte réseau sans fil WiFi de mon ordinateur
String serverName = "http://192.168.253.77:1880";

//Variables d'enregistrement de la postion dans le temps et du délais d'exécution du code
unsigned long lastTime = 0;
unsigned long timerDelay = 1000;

int led_state = 0;

void setup() {
  //On définit le baudrate
  Serial.begin(115200);
  //Configuration du pin de la led en sortie
  pinMode(LED_BUILTIN, OUTPUT);
  //LED_BUILTIN est une constante prédéfinie qui permet de se relier directement au pin de la led sans connaître son numéro


  // Initialisation du capteur
  dht.begin();

  // Connection au WiFi
  WiFi.begin(ssid, password);
  //Affichage du statut de la connection dans le Serial Monitor
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void change_led_state(){
  //On teste la connection avant d'essayer d'envoyer une requête
  if(WiFi.status() != WL_CONNECTED) {
      Serial.println("WiFi Disconnected");
      return;
  }
  WiFiClient client;
  HTTPClient http;

  String serverPath = serverName + "/get-led_state";
  http.begin(client, serverPath.c_str());
  int httpCode = http.GET();

  //S'il n'y a pas d'erreur on récupère les informations contenues dans le payload
    if (payload.indexOf("\"led_state\":1") != 1) {
      digitalWrite(LED_BUILTIN, LOW); // LED on
      Serial.println("LED is on");
    } else {
      digitalWrite(LED_BUILTIN, HIGH); // LED off
      Serial.println("LED is off");
    }
   else {
    Serial.printf("HTTP POST failed, error: %s\n", http.errorToString(httpCode).c_str());
  }

}

void loop() {
  //Boucle pour exécuter le code tous les timerDelay, 1s, milis() compte le nombre de ms
  //Cette boucle est un timer
  if((millis() - lastTime) > timerDelay) {
    //il s'agit de pulling pour changer l'état de la LED
    //ce n'est pas le serveur qui envoie le changement d'état de l'interrupteur à chaque fois 
    //qu'il y en a un mais l'ESP qui récupère l'état de l'interrupteur tous les timerDelay
    change_led_state();
    //Enregistrement de la position temporelle 
    lastTime = millis();
  }
}
