from machine import Pin, PWM
from time import sleep

# frequency = 1000=一秒1000次
# 當duty_cycle=0時，LED熄滅
# 當duty_cycle=512時，代表每一次都只亮一半，總共重複了1000次，所以看起來是半亮
# 當duty_cycle=1023時，代表每一次都亮，總共重複了1000次，所以看起來是全亮
# 這是PWM的特性

frequency = 1000
duty_cycle = 0
led = PWM(Pin(2), freq=frequency, duty=duty_cycle)
while True:
    led.duty(0)
    sleep(99)
    led.duty(512)
    sleep(99)
    led.duty(923)
    sleep(99)
