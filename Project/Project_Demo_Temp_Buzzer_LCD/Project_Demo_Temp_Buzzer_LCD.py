# https://realpython.com/intro-to-python-threading/
import logging
import threading
import time
import lcd_i2c_lib

#Add DS18B20 pin 19 (see demo_Read_DS18B20_kxn.py)
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

#Add MKL_DHT11 pin 17----------------------------------
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17, False)

#=================End Import zone=========================

temDHT = 0
temDS18B20 = 0

#=================End Global variable zone================

def helloWorld():
    while(1):
        logging.info("Hello")
        time.sleep(3);
#=================End Function zone================
    
def thread_function_readDHT(name):
    global temDHT
    while(1):
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            
            temDHT = temperature_c
            logging.info("Thread %s: starting read DHT11: %d", name, temDHT)
            
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
        #logging.info("Thread %s: finishing, number %d", name, number)
    
def thread_function_readDS18B20(name):
    global temDS18B20
    while(1):
        temDS18B20= sensor.get_temperature()
        logging.info("Thread %s: starting read DS18B20: %d", name, temDS18B20)
        
        time.sleep(1)
        #logging.info("Thread %s: finishing, number %d", name, number)
        
def thread_function_showI2C_LCD(name):
    global temDS18B20
    while(1):
        #helloWorld()
        # Send some more text
        stringLine_1 = "DS18B20 value: %0.1f" %(temDS18B20)
        stringLine_2 = "DHT T: %0.1f" %(temDHT)
        
        lcd_i2c_lib.lcd_string(stringLine_1, lcd_i2c_lib.LCD_LINE_1)
        lcd_i2c_lib.lcd_string(stringLine_2, lcd_i2c_lib.LCD_LINE_2)
        
        #logging.info("Thread %s: starting show LCD DHT: %d, DS: %d", name, temDHT,temDS18B20)
        time.sleep(0.2)
        #logging.info("Thread %s: finishing, number %d", name, number)
#=================End define Thread zone=========================







    
#=======================================================
# Program
if __name__ == "__main__":
    # define show debug
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    # step 1: create thread list
    threads = list()
    
    #step 2: add function to theads list
    x = threading.Thread(target=thread_function_readDHT, args=("DHT11",))
    threads.append(x)
    x.start()
    
    x = threading.Thread(target=thread_function_readDS18B20, args=("DS18B20",))
    threads.append(x)
    x.start()
    
    lcd_i2c_lib.lcd_init()
    x = threading.Thread(target=thread_function_showI2C_LCD, args=("showLCD",))
    threads.append(x)
    x.start()
    
    
    
    