# describe
this package ust to control L9110-I2C by Raspberry pi

# install package
1. Create virtual environment: `python3 -m venv your_yenv`
2. Activate virtual environment: `source your_yenv/bin/activate`
3. install package: `pip install MKE-M17`

# How to use `MKE_M17` lib

## Initialize an L9110 I2C driver

**Parameters:**

* `i2c_address` (int): The I2C address of the L9110 chip. Default is `0x40`.
* `i2c_bus_number` (int): The number of the I2C bus to use. Default is `1`.

**Example:**
> your_yenv/bin/python3.11

```python
from MKE_M17 import L9110

# Initialize l9110 object with default address and default i2c bus
l9110 = L9110()

# Initialize object l9110 with address 0x42 and i2c bus 1
l9110 = L9110(i2c_address=0x42, i2c_bus_number=1)
```
## rc_data_send(rc_motor, degree)
**Args:**

* `rc_motor` (int): 1 for S1 or 2 for S2.
* `degree` (int): 0-180 of the servo's position.

**Returns:**
> list: A list of data to be sent via i2c.

**Example:**
```python
#control servo 1 with 150 degree
servo1 = l9110.rc_data_send(1, 150)
#control servo 2 with 90 degree
servo2 = l9110.rc_data_send(2, 90)
```

## dc_data_send(dc, percent, direction)
**Args:**

* `dc` (int): 0 for MA or 1 for MB.
* `percent` (int): Speed percentage (0-100) of the DC motor.
* `direction` (int): 0 for clockwise (CW) or 1 for counterclockwise (CCW).

**Returns:**
> list: A list of data to be sent via i2c.

**Example:** 
```python
# control DC motor A with 50% speed and clockwise
motorA = l9110.dc_data_send(0, 50, 0)
# control DC motor B with 70% speed and counterclockwise
motorB = l9110.dc_data_send(1, 70, 1)
```

## set_address(old_address, new_address)
> Change the I2C address of the L9110 device.

**Args:**
* `old_address` (byte): The current I2C address of the device.
* `new_address` (byte): The new I2C address to be set for the device.

**Raises:**
> IOError: If there is an error in communication with the device.

**Example:**
```python
#set i2c address to 0x42
set_address(0x40, 0x42)
```
> Set address successful\
> New address is: 0x42
## send_i2c_data(data)
**Args:**
* `data` (list): A list of data to be sent via i2c.

**Raises:**
> IOError: If there is an error in communication with the device.

**Example:**
```python
l9110.send_i2c_data(motorA)
l9110.send_i2c_data(motorB)
l9110.send_i2c_data(servo1)
l9110.send_i2c_data(servo2)
```
