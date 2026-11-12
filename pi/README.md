# Raspberry Pi code

This folder runs on the Raspberry Pi, not on the website server.

## Wiring

Pin numbers are BCM (GPIO) numbers. Change them in `config.py` if you use different pins.

| Part | Connect to |
|------|------------|
| DHT11 data pin | GPIO17 (with a 10 kΩ pull-up to 3.3 V if your DHT11 is not on a small board) |
| DHT11 VCC / GND | 3.3 V / GND |
| ADC module SDA / SCL | GPIO2 (SDA) / GPIO3 (SCL) |
| ADC module VCC / GND | 3.3 V / GND |
| Photoresistor | ADC input A0, with a 10 kΩ resistor as a voltage divider |

## Setup on the Pi

1. Turn on I2C: `sudo raspi-config` → Interface Options → I2C → Yes, then reboot.
2. Check the ADC is found: `i2cdetect -y 1` should show `48` or `4b`.
3. Install the libraries:
   ```
   sudo apt install python3-venv libgpiod2
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Run

```
python3 plant_pi.py
```

It prints the temperature, humidity and light every 10 seconds. Press Ctrl+C to stop.

If the light reading goes up when you cover the photoresistor, set `INVERT_LIGHT = True` in `config.py`.
