# ESP8266 Template Project

This is a template that is the base of all my ESP8266 projects.  Once this project is built and flashed onto any ESP8266 device **once**, all subsequent updates can be done over-the-air (OTA).

I've used a lot of [ESP-12F](https://www.google.com/search?q=esp-12f)'s in my projects, which is a bare bones ESP8266 module (as can be seen in the pictures) for which all the connecting wires have to be soldered and code flashed to it using a USB-to-Serial Adapter like '[FT232RL USB to TTL 3.3V 5.5V Serial Adapter Module for Arduino](https://www.google.co.in/search?q=FT232RL+USB+to+TTL+3.3V+5.5V+Serial+Adapter+Module+for+Arduino)' as described in section 3.1 [here](https://circuitjournal.com/esp8266-with-arduino-ide).  Starting with this template will require all the USB-to-Serial stuff and the flash setup of the ESP-12F to be done just once and then everything else can be done over-the-air from then on, significantly simplifying the development process.

Here is what is in this base project:

- [WiFiManager](https://www.arduino.cc/reference/en/libraries/wifimanager/) library so that the actual wifi network that the device connects to can be configured at any time later
- [ArduinoOTA](https://www.arduino.cc/reference/en/libraries/arduinoota/) library that provides all the over-the-air (OTA) capabilities
- Built-in [ESP8266WebServer](https://github.com/esp8266/Arduino/tree/master/libraries/ESP8266WebServer) Arduino library that provides basic web request capability to check version, enable/disable OTA updates, etc

The OTA hostname and password can be set in the  `setup()` function.  This is the hostname that is visible via `mDNS` and the password that needs to be provided to authenticate the OTA update command:

```
...
    ArduinoOTA.setHostname("hostname");
    ArduinoOTA.setPassword("ota-password");
...
```

The local device wifi ssid and password can be set in the `wifiConnect` function.  This is the device network that you can connect to initially and 'WiFiManager' will allow you to configure the actual wifi network that the device needs to connect to after that:

```
...
    wifiManager.autoConnect("device-wifi-ssid", "device-wifi-password");
...
```

The project can be built using `./build.sh`, which executes the following:

```
arduino-cli compile --fqbn esp8266:esp8266:generic .
```

Any OTA updates (after the initial flashing is done), can be done using:

```
python3 espota.py -i <ip/hostname> -f <location_of_project.ino.bin> -a <ota-password>
```

The `espota.py` can be found in the tools folder of the corresponding board of your Arduino installation.  For example, on my Raspberry Pi, for `esp8266` devices, it is under `~/.arduino15/packages/esp8266/hardware/esp8266/2.7.4/tools/espota.py`

OTA mode can be enabled on the device by running:

```
wget -q -O /dev/null 'http://<ip/hostname>/ota?on'
```

after which the `espota.py` command can be run to update the new build over OTA.

The current version of the code, the device MAC address can be queried using:

```
wget 'http://<ip/hostname>/version'
```

