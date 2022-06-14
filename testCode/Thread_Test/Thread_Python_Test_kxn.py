# https://realpython.com/intro-to-python-threading/
import logging
import threading
import time

#global temDHT
#global temDS18B20

temDHT = 0
temDS18B20 = 0
    
def thread_function_readDHT(name):
    global temDHT
    while(1):
        temDHT= temDHT+10
        logging.info("Thread %s: starting read DHT: %d", name, temDHT)
        
        time.sleep(2)
        #logging.info("Thread %s: finishing, number %d", name, number)
    
def thread_function_readDS18B20(name):
    global temDS18B20
    while(1):
        temDS18B20= temDS18B20+100
        logging.info("Thread %s: starting read DS18B20: %d", name, temDS18B20)
        
        time.sleep(1)
        #logging.info("Thread %s: finishing, number %d", name, number)
        
def thread_function_showI2C_LCD(name):
    while(1):
        logging.info("Thread %s: starting show LCD DHT: %d, DS: %d", name, temDHT,temDS18B20)
        time.sleep(0.2)
        #logging.info("Thread %s: finishing, number %d", name, number)

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
    
    x = threading.Thread(target=thread_function_showI2C_LCD, args=("showLCD",))
    threads.append(x)
    x.start()
