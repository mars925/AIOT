#########################匯入模組#########################
from machine import Pin, ADC
from time import sleep
import class5.mcu as mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
frequency = 1000
duty_cycle = 0


gpio = mcu.gpio()
light_sensor = ADC(0)
RED = pwm(gpio.D5, Pin.OUT)
GREEN = pwm(gpio.D6, Pin.OUT)
BLUE = pwm(gpio.D7, Pin.OUT)

RED.value(0)
GREEN.value(0)
BLUE.value(0)

#########################主程式#############################

while True:
    light_sensor_reading = light_sensor.read()
    print(f"value= {light_sensor_reading}, {round(light_sensor_reading * 100 / 1024)}%")
    sleep(1)
    if light_sensor_reading > 700:
        GREEN.value(1)
    else:
        GREEN.value(0)
RED.duty(duty_cycle)
GREEN.duty(duty_cycle)
BLUE.duty(duty_cycle)
