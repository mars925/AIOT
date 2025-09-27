#########################匯入模組#########################
from machine import Pin, PWM
from time import sleep
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
frequency = 1000
duty_cycle = 0
gpio = mcu.gpio()
RED = PWM(Pin(gpio.D5), freq=frequency, duty=duty_cycle)
GREEN = PWM(Pin(gpio.D6), freq=frequency, duty=duty_cycle)
BLUE = PWM(Pin(gpio.D7), freq=frequency, duty=duty_cycle)

#########################主程式#########################
while True:
    for duty_cycle in range(1023, -1, -1):
        RED.duty(duty_cycle)
        GREEN.duty(1023 - duty_cycle)
        sleep(0.001)
    for duty_cycle in range(1023, -1, -1):
        GREEN.duty(duty_cycle)
        BLUE.duty(1023 - duty_cycle)
        sleep(0.001)

    for duty_cycle in range(1023, -1, -1):
        BLUE.duty(duty_cycle)
        RED.duty(1023 - duty_cycle)
        sleep(0.001)
