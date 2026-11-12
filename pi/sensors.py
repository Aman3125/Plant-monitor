"""Read the plant monitor sensors on the Raspberry Pi.

- DHT11: temperature (°C) and humidity (%)
- Photoresistor through the ADC module: light level (0-100 %)
"""
import time

import adafruit_dht
import board
from smbus2 import SMBus

import config

# I2C addresses of the two ADC chips used in Raspberry Pi starter kits
PCF8591_ADDRESS = 0x48
ADS7830_ADDRESS = 0x4B


class ADC:
    """Reads a value from 0 to 255 from the ADC module.

    Works with both the PCF8591 and the ADS7830 chip, and finds out
    by itself which one is connected.
    """

    def __init__(self, bus_number: int = config.I2C_BUS):
        self.bus = SMBus(bus_number)
        if self._is_connected(ADS7830_ADDRESS):
            self.address, self.chip = ADS7830_ADDRESS, "ADS7830"
        elif self._is_connected(PCF8591_ADDRESS):
            self.address, self.chip = PCF8591_ADDRESS, "PCF8591"
        else:
            raise RuntimeError("No ADC module found on I2C. Check the wiring and that I2C is turned on.")

    def _is_connected(self, address: int) -> bool:
        try:
            self.bus.read_byte(address)
            return True
        except OSError:
            return False

    def read(self, channel: int) -> int:
        if self.chip == "ADS7830":
            # Single-ended input, the channel bits are in a special order on this chip
            command = 0x84 | (((channel << 2 | channel >> 1) & 0x07) << 4)
            return self.bus.read_byte_data(self.address, command)
        # PCF8591: select the channel, then read twice because the first value is the old one
        self.bus.write_byte(self.address, 0x40 | channel)
        self.bus.read_byte(self.address)
        return self.bus.read_byte(self.address)

    def close(self):
        self.bus.close()


class Sensors:
    """All the sensors on the plant monitor in one place."""

    def __init__(self):
        self.dht = adafruit_dht.DHT11(getattr(board, f"D{config.DHT11_PIN}"))
        self.adc = ADC()

    def read_temperature_and_humidity(self, attempts: int = 5):
        """Return (temperature, humidity), or (None, None) if the DHT11 does not answer.

        The DHT11 often misses a reading, so it is tried a few times.
        """
        for _ in range(attempts):
            try:
                temperature = self.dht.temperature
                humidity = self.dht.humidity
                if temperature is not None and humidity is not None:
                    return float(temperature), float(humidity)
            except RuntimeError:
                pass
            # The DHT11 needs about 2 seconds between readings
            time.sleep(2)
        return None, None

    def read_light(self) -> float:
        """Return the light level from 0 (dark) to 100 (bright)."""
        value = self.adc.read(config.LIGHT_ADC_CHANNEL)
        percent = value / 255 * 100
        if config.INVERT_LIGHT:
            percent = 100 - percent
        return round(percent, 1)

    def read_all(self) -> dict:
        """Return every reading, using the same sensor names as the website."""
        temperature, humidity = self.read_temperature_and_humidity()
        return {
            "temperature": temperature,
            "humidity": humidity,
            "light": self.read_light(),
        }

    def close(self):
        self.dht.exit()
        self.adc.close()
