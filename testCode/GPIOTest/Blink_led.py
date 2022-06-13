#https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-example

import RPi.GPIO as GPIO
import time

# Pin Definitons:
ledPin = 19 # Broadcom pin 23 (P1 pin 16)

dc = 100 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

# Initial state for LEDs:
GPIO.output(ledPin, GPIO.LOW)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(1.0);
    
        GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(1)
            
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    pwm.stop() # stop PWM
    GPIO.cleanup() # cleanup all GPIO