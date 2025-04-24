from machine import Pin, SoftI2C
from bh1750 import BH1750
import time

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=400000)

sensor = BH1750(bus=i2c, addr=0x23)
try:
    while True:
        lux = sensor.luminance(BH1750.CONT_HIRES_1)
        print("Luminance: {:.2f} lux".format(lux))
        time.sleep(2)

except Exception as e:
    print("Error:", e)
