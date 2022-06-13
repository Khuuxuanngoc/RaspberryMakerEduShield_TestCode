"""
    Step 1: Edit config.txt
            Add two line:
                dtoverlay=w1-gpio
                dtoverlay=w1-gpio,gpiopin=19
    Step 2: Install library
            sudo pip3 install w1thermsensor
            (https://bigl.es/ds18b20-temperature-sensor-with-python-raspberry-pi/)
            
    Step 3: Connect DS18B20 to GPIO19 then Run the code
"""


import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)