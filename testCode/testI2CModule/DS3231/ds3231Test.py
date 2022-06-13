# Link https://pypi.org/project/adafruit-circuitpython-ds3231/

import busio
import adafruit_ds3231
import time

from board import *

myI2C = busio.I2C(SCL, SDA)

rtc = adafruit_ds3231.DS3231(myI2C)

#set time 
#rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))

t = rtc.datetime
print(t)
print(t.tm_hour, t.tm_min)