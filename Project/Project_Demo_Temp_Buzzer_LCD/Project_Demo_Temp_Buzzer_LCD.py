import time


#Add DS18B20 pin 19 (see config.txt)
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

#Add MKL_DHT11 pin 17----------------------------------
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17)

def getDHTData():
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        """
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        """

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
    
#=======================================================
# Program
while True:
    temperature_DS18B20 = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature_DS18B20)
    time.sleep(1)