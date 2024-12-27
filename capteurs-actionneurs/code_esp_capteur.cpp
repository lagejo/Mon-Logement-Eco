#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "DHT.h" // Assurez-vous d'utiliser la bonne bibliothèque pour le capteur DHT

// Préciser de quel DHT il s'agit et sur quel pin
#define DHTTYPE DHT11
#define DHTPIN 0 // Utilisez le bon pin pour votre configuration
DHT dht(DHTPIN, DHTTYPE);

// Connection au réseau WiFi
const char* ssid = "Redmi Note 12 Pro";
const char* password = "spaghetti";
// Adresse IP locale de votre ordinateur sur le réseau
String serverName = "http://192.168.217.77:8000/capteur"; // Remplacez par l'adresse IP locale de votre ordinateur

// Variables d'enregistrement de la position dans le temps et du délai d'exécution du code
unsigned long lastTime = 0;
unsigned long timerDelay = 10000; // 10 secondes

void setup() {
  // On définit le baudrate
  Serial.begin(115200);
  // Configuration du pin de la LED en sortie

  // Initialisation du capteur
  dht.begin();

  // Connection au WiFi
  WiFi.begin(ssid, password);
  // Affichage du statut de la connection dans le Serial Monitor
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void sendPostRequest() {
  // On teste la connection avant d'essayer d'envoyer une requête
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi Disconnected");
    return;
  }

  WiFiClient client;
  HTTPClient http;

  // Transmission des informations du capteur au Serial Monitor pour pouvoir vérifier son fonctionnement même si la connection n'est pas établie
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT capteur!");
    return;
  }

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C");

  http.begin(client, serverName);
  http.addHeader("Content-Type", "application/json");

  // Conversion en string du premier élément pour que toutes les données soient ensuite concaténées
  String postData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";

  int httpResponseCode = http.POST(postData);

  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);

  http.end();
}

void loop() {
  // Boucle pour exécuter le code tous les timerDelay, 10s, millis() compte le nombre de ms
  // Cette boucle est un timer
  if ((millis() - lastTime) > timerDelay) {
    sendPostRequest();
    lastTime = millis();
  }
}