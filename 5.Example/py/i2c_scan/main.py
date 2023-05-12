from time import sleep
from machine import Pin, I2C, SoftI2C

i2c = I2C(0, scl=Pin(10), sda=Pin(18), freq=400_000)
# i2c = SoftI2C(scl=Pin(10), sda=Pin(18), freq=400_000)

while True:
    for device in i2c.scan():
        print(device, hex(device))
    sleep(2)
