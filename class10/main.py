#########################匯入模組#########################
from umqtt.simple import MQTTClient
import sys
import time
import mcu
from machine import ADC


#########################函式與類別定義#########################
def on_message(topic, msg):
    global m
    msg = msg.decode("utf-8")  # Byte to str
    topic = topic.decode("utf-8")
    print(f"my subscribe topic:{topic}, msg:{msg}")
    m = msg


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("Singular_AI", "Singular#1234"):
    print(f"IP={wi.ip}")

mq_server = "mqtt.singularinnovation-ai.com"
# mq_server = "192.168.68.114"
mqttClientId = "mars"  # 大家要不一樣, 只使用英文, 不要使用中文或特殊符號
mqtt_username = "singular"  # 這是登入伺服器的帳號, 大家都一樣
mqtt_password = "Singular#1234"  # 這是登入伺服器的密碼, 大家都一樣
mqtt = mcu.MQTT(mqttClientId, mq_server, mqtt_username, mqtt_password, keepalive=60)
mqtt.connect()
mqtt.subscribe("ori", on_message)  # 訂閱主題, 有訊息時呼叫 on_message 函式
gpio = mcu.gpio()
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7, pwm=False)
LED.LED_open(0, 0, 0)
light = ADC(0)
m = ""
#########################主程式#########################

while True:
    # 查看是否有訂閱主題發布的資料
    mqtt.check_msg()
    if m == "ON":
        LED.LED_open(1, 1, 1)
    elif m == "OFF":
        LED.LED_open(0, 0, 0)
    elif m == "AUTO":
        if light.read() > 700:
            LED.LED_open(1, 1, 1)
    else:
        LED.LED_open(0, 0, 0)
    time.sleep(0.1)
