# ESP8266-12F	 

## Pins

Antenna to LEFT, facing UP

```
Top:	TX	RX	5	4	0	2	15	GND  
Buttom:	RST	ADC	EN	16	14	12	13	VCC
```

## ESP <-> FT232RL connections

```
Rx <-> Tx  
Tx <-> Rx  
Gnd <-> Gnd
```

> Note: No power / Vcc from FT232RL to ESP

## ESP connections

### Fixed  

```
GPIO15 -> Low  
GPIO2 -> High  
EN -> High  
VCC -> 3.3v  
GND -> Gnd
```

### Floating  

```
GPIO0 -> Low (Program)  
GPIO0 -> Floating (Run) - High to run??  
RST -> Low (Program, start of upload)  
RST -> Floating (Run)
```

### Minimum to RUN:

```
3.3v VCC
GND
EN -> High
GPIO15 -> Low (at boot???)
```

# ESP8266-01

- To program:
  - Same as above except:
  - There is no GPIO15

- To run:
  - Same as above except:  
  - There is no GPIO15

```
3.3v VCC
GND
EN -> High
```
