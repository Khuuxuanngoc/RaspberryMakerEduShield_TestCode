from L9110_I2C import L9110
from time import sleep

l9110 = L9110()

servo_data = l9110.rc_data_send(l9110.S1, 150)  
l9110.send_i2c_data(servo_data)
sleep(1)

dc_data = l9110.dc_data_send(l9110.MA, 50, l9110.CW)
l9110.send_i2c_data(dc_data)
sleep(2)

dc_data = l9110.dc_data_send(l9110.MA, 0, l9110.CW)
l9110.send_i2c_data(dc_data)
