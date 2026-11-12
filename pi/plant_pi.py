"""Main program for the Raspberry Pi plant monitor.

Run it on the Pi with:  python3 plant_pi.py
Stop it with Ctrl+C.
"""
import time
from datetime import datetime

import config
from sensors import Sensors


def main():
    sensors = Sensors()
    print(f"Plant monitor started. ADC chip: {sensors.adc.chip}. Reading every {config.READ_INTERVAL_SECONDS} s.")
    try:
        while True:
            readings = sensors.read_all()
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] temperature={readings['temperature']} °C  "
                  f"humidity={readings['humidity']} %  light={readings['light']} %")
            time.sleep(config.READ_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        sensors.close()


if __name__ == "__main__":
    main()
