#########################匯入模組#########################
from machine import Pin
from time import sleep
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
RED = Pin(gpio.D5, Pin.OUT)
GREEN = Pin(gpio.D6, Pin.OUT)
BLUE = Pin(gpio.D7, Pin.OUT)

RED.value(0)
GREEN.value(0)
BLUE.value(0)
#########################主程式#########################
while True:
    GREEN.value(1)
    sleep(1)
    RED.value(1)
    sleep(1)
    GREEN.value(0)
    sleep(1)
    RED.value(0)
