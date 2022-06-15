#-*- coding: utf-8 -*-

# https://realpython.com/intro-to-python-threading/
import logging
import threading
import time
import lcd_i2c_lib
import RPi.GPIO as GPIO

#Add Alarm pint output
# Pin Definitons:
ledPin = 18 # Broadcom pin 23 (P1 pin 16)
LED_ON = GPIO.HIGH
LED_OFF = GPIO.LOW
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

# Initial state for LEDs:
GPIO.output(ledPin, LED_OFF)


#Add DS18B20 pin 19 (see demo_Read_DS18B20_kxn.py)
from w1thermsensor import W1ThermSensor
#sensor = W1ThermSensor()

#Add MKL_DHT11 pin 17----------------------------------
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17, False)

#=================End Import zone=========================

temDHT = 0
humDHT = 0
temDS18B20 = 0
temAlarm = 33.0
b_EnAlrm = False

#=================End Global variable zone================

def helloWorld():
    while(1):
        logging.info("Hello")
        time.sleep(3);
#=================End Function zone================
    
def thread_function_readDHT(name):
    global temDHT
    global humDHT
    while(1):
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            
            temDHT = temperature_c
            humDHT = humidity
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
    sensor = W1ThermSensor()
    while(1):
        try:
            temDS18B20= sensor.get_temperature()
            logging.info("Thread %s: starting read DS18B20: %d", name, temDS18B20)
        except:
            sensor = W1ThermSensor()
            
        
        time.sleep(1)
        #logging.info("Thread %s: finishing, number %d", name, number)
        
def thread_function_showI2C_LCD(name):
    global temDS18B20
    global humDHT
    global temDHT
    global temAlarm
    global b_EnAlrm
    
    stringLine_1 = "Air Temp & Humidity"
    stringLine_3 = "FishTank Temperature"
    
    lcd_i2c_lib.lcd_string(stringLine_1, lcd_i2c_lib.LCD_LINE_1)
    lcd_i2c_lib.lcd_string(stringLine_3, lcd_i2c_lib.LCD_LINE_3)
    
    while(1):
        # Send some more text
        #stringLine_1 = "DS18B20 value: %0.1f " %(temDS18B20)
        #stringLine_2 = "DHT T: %0.1f%cC " %(temDHT, chr(223))
        #stringLine_3 = "DHT H: %0.1f%% " %(humDHT)
        
        stringLine_2 = "%0.1f%cC %0.1f%% " %(temDHT, chr(223), humDHT)
        stringLine_4 = "%0.1f%cC  AL:%0.1f%cC  " %(temDS18B20, chr(223), temAlarm, chr(223))
        
        stringTemDHT = "%0.1f%cC  "%(temDHT, chr(223))
        stringHumDHT = "%0.1f%%  "%(humDHT)
        stringTemDS18B20 = "%0.1f%cC  "%(temDS18B20, chr(223))
        stringTemAlarm = "AL:%0.1f%cC "%(temAlarm, chr(223))
        
        
        #lcd_i2c_lib.lcd_string(stringLine_1, lcd_i2c_lib.LCD_LINE_1)
        #lcd_i2c_lib.lcd_string(stringLine_2, lcd_i2c_lib.LCD_LINE_2)
        
        #lcd_i2c_lib.lcd_string(stringLine_3, lcd_i2c_lib.LCD_LINE_3)
        #lcd_i2c_lib.lcd_string(stringLine_4, lcd_i2c_lib.LCD_LINE_4)
        lcd_i2c_lib.lcd_string_at(stringTemDHT, 1,1)
        lcd_i2c_lib.lcd_string_at(stringHumDHT, 12,1)
        
        lcd_i2c_lib.lcd_string_at(stringTemDS18B20, 1,3)
        lcd_i2c_lib.lcd_string_at(stringTemAlarm, 10,3)
        
        if (temDS18B20) >= temAlarm:
            b_EnAlrm = True
            logging.info("Warning En Alarm")
        else:
            b_EnAlrm = False
        #logging.info("Thread %s: starting show LCD DHT: %d, DS: %d", name, temDHT,temDS18B20)
        time.sleep(0.2)
        #logging.info("Thread %s: finishing, number %d", name, number)
        
def thread_function_Alrm(name):
    global b_EnAlrm
    global temAlarm
    global temDS18B20
    global temDHT
    global LED_ON
    global LED_OFF
    while(1):
        if b_EnAlrm == True:
            logging.info("Thread %s: starting alarm output: %d", name, 1)
            GPIO.output(ledPin, LED_ON)
            
            time.sleep(0.1)
            #logging.info("Thread %s: starting alarm output: %d", name, 0)
            GPIO.output(ledPin, LED_OFF)
            time.sleep(0.1);
        else:
            GPIO.output(ledPin, LED_OFF)
            
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
    
    x = threading.Thread(target=thread_function_Alrm, args=("AlamOut",))
    threads.append(x)
    x.start()
    
    
    
    
    