#########################匯入模組#########################
import time
import mcu
from machine import ADC

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
light_sensor = ADC(0)

#########################主程式#########################
while True:
    mqtt.publish("ori", str(light_sensor.read()))
    time.sleep(1)