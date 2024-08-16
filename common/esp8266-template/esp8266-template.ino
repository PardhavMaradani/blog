#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

ESP8266WebServer server(80);

void handle_version();
void handle_ota_mode();

String version = "1.0";
bool otaUpdateMode = false;
bool debug = true;

WiFiManager wifiManager;

void setup() {
    if (debug) {
        Serial.begin(115200);
    }
    Serial.println("setup");

    wifiConnect();

    ArduinoOTA.setPort(8266);
    ArduinoOTA.setHostname("hostname");
    ArduinoOTA.setPassword("ota-password");
    ArduinoOTA.onStart([]() {
        Serial.println("OTA start");
    });
    ArduinoOTA.onEnd([]() {
        Serial.println("OTA end");
    });
    ArduinoOTA.onError([](ota_error_t error) {
        Serial.println("OTA error : " + String(error));
    });
    ArduinoOTA.begin();

    server.on("/version", [&]() {
        handle_version();
    });
    server.on("/ota", [&]() {
        handle_ota_mode();
    });
    server.begin(); 

    Serial.println("setup done");
}

void wifiConnect() {
    WiFi.mode(WIFI_STA);
    wifiManager.setConfigPortalTimeout(180);
    wifiManager.autoConnect("device-wifi-ssid", "device-wifi-password");
    unsigned long s = millis();
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        if (millis() - s > 300000) {
            ESP.restart();
        }
    }
    WiFi.setAutoReconnect(true);
}

void loop() {
    server.handleClient();
    if (otaUpdateMode) {
        ArduinoOTA.handle();
    }
}

void handle_version() {
    server.send(200, "text/plain", version + "," + ArduinoOTA.getHostname() + "," + WiFi.macAddress());
}

void handle_ota_mode() {
    if (server.args() == 1 && server.hasArg("on")) {
        otaUpdateMode = true;
    }
    if (server.args() == 1 && server.hasArg("off")) {
        otaUpdateMode = false;
    }
    server.send(200, "text/plain", "");
}
