from machine import Pin
from time import sleep

p2 = Pin(2, Pin.OUT)

while True:
    p2.value(0)
    sleep(1)
    p2.value(1)
    sleep(1)
