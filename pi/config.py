"""Settings for the Raspberry Pi side of the plant monitor.

Change the pin numbers here if you wire the parts to different pins.
Pin numbers are BCM (GPIO) numbers, not the physical pin positions.
"""

# DHT11 temperature and humidity sensor (data pin)
DHT11_PIN = 17

# The ADC module is on the I2C bus (SDA = GPIO2, SCL = GPIO3)
I2C_BUS = 1
# ADC channel the photoresistor is connected to (A0 = 0)
LIGHT_ADC_CHANNEL = 0
# Set to True if the light reading goes UP when you cover the photoresistor
INVERT_LIGHT = False

# How often to take a reading, in seconds
READ_INTERVAL_SECONDS = 10
