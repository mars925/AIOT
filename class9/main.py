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
    show_msg = f"topic:{topic}, msg:{msg}"
    print(show_msg)


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
mqClient0 = MQTTClient(
    mqttClientId, mq_server, user=mqtt_username, password=mqtt_password, keepalive=30
)

try:
    mqClient0.connect()
except:
    sys.exit()
finally:
    print("connected MQTT server")


mqClient0.set_callback(on_message)  # 設定接收訊息的時候要呼叫的函式
mqClient0.subscribe("ori")  # 設定想訂閱的主題
gpio = mcu.gpio()
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7, pwm=False)
LED.LED_open(0, 0, 0)
light = ADC(0)
m = ""
#########################主程式#########################

while True:
    # 查看是否有訂閱主題發布的資料
    mqClient0.check_msg()  # 等待已訂閱的主題發送資料
    mqClient0.ping()  # 持續確認是否還保持連線
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
