#########################匯入模組#########################
from umqtt.simple import MQTTClient
import sys
import time
import mcu
from machine import ADC, I2C, Pin
import ssd1306


#########################函式與類別定義#########################
def on_message(topic, msg):
    global m
    msg = msg.decode("utf-8")  # Byte to str
    topic = topic.decode("utf-8")
    print(f"my subscribe topic:{topic}, msg:{msg}")
    m = msg


def oled_text_multiline(oled, text, x=0, y=0):
    """在 SSD1306 上做簡單的換行顯示。
    - text 支援手動換行字元 '\n'。
    - 會根據顯示器寬度自動換行（每字元約 8px 寬）。
    - 多出來的行會被截斷以避免超出顯示範圍。
    """
    if text is None:
        return
    text = str(text).replace("\r", "")
    max_chars = oled.width // 8
    max_lines = oled.height // 8
    lines = []
    for para in text.split("\n"):
        # 以單字包裝，避免隨便在中間斷字
        words = para.split(" ")
        cur = ""
        for w in words:
            if cur == "":
                candidate = w
            else:
                candidate = cur + " " + w
            if len(candidate) <= max_chars:
                cur = candidate
            else:
                if cur != "":
                    lines.append(cur)
                # 若單一字就超過限制，則硬切
                while len(w) > max_chars:
                    lines.append(w[:max_chars])
                    w = w[max_chars:]
                cur = w
        if cur != "":
            lines.append(cur)

    # 顯示時若超過高度則截斷
    for i, line in enumerate(lines[:max_lines]):
        oled.text(line, x, y + i * 8)


def _char_width(c):
    # 粗略估算：ASCII 字元寬度 1，非 ASCII（如中文）視為 2
    try:
        return 1 if ord(c) < 128 else 2
    except Exception:
        return 1


def oled_text_paginate(oled, text):
    """將文字包裝為多頁，每頁不超過顯示可容納的行數與每行字元數。
    回傳值：list of pages, 每頁為 list of lines (str)。
    """
    if text is None or text == "":
        return [[""]]

    text = str(text).replace("\r", "")
    max_width = oled.width
    max_chars = max_width // 8
    max_lines = oled.height // 8

    # 先將文字分為可顯示的行，支援手動換行
    lines = []
    for para in text.split("\n"):
        cur = ""
        cur_w = 0
        for ch in para:
            w = _char_width(ch)
            if cur_w + w <= max_chars:
                cur += ch
                cur_w += w
            else:
                if cur != "":
                    lines.append(cur)
                # 若單字元就超過長度，強制分割
                if w > max_chars:
                    # 以簡單方式切割過長字串（極少發生）
                    part = ch
                    lines.append(part)
                    cur = ""
                    cur_w = 0
                else:
                    cur = ch
                    cur_w = w
        if cur != "":
            lines.append(cur)

    # 分頁
    pages = []
    for i in range(0, len(lines), max_lines):
        pages.append(lines[i : i + max_lines])
    if not pages:
        pages = [[""]]
    return pages


def oled_show_page(oled, page_lines, x=0, y=0):
    oled.fill(0)
    for i, line in enumerate(page_lines):
        oled.text(line, x, y + i * 8)
    oled.show()


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
i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#########################主程式#########################

# 分頁顯示相關狀態
previous_m = None
oled_pages = [[""]]
oled_page_idx = 0
page_display_time = 1.5
last_page_time = time.time()

while True:
    mqtt.check_msg()

    # 當消息改變時重建分頁
    if m != previous_m:
        oled_pages = oled_text_paginate(oled, m)
        oled_page_idx = 0
        last_page_time = time.time()
        previous_m = m

    # 顯示當前頁面（若只有一頁即固定顯示）
    oled_show_page(oled, oled_pages[oled_page_idx])

    # 多頁自動翻頁
    if len(oled_pages) > 1 and (time.time() - last_page_time) > page_display_time:
        oled_page_idx = (oled_page_idx + 1) % len(oled_pages)
        last_page_time = time.time()

    # LED 控制邏輯
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
