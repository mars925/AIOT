import network
import sys
from machine import PWM, Pin
from umqtt.simple import MQTTClient


class gpio:
    def __init__(self):
        self._D0 = 16
        self._D1 = 5
        self._D2 = 4
        self._D3 = 0
        self._D4 = 2
        self._D5 = 14
        self._D6 = 12
        self._D7 = 13
        self._D8 = 15
        self._SDD3 = 10
        self._SDD2 = 9

    @property
    def D0(self):
        return self._D0

    @property
    def D1(self):
        return self._D1

    @property
    def D2(self):
        return self._D2

    @property
    def D3(self):
        return self._D3

    @property
    def D4(self):
        return self._D4

    @property
    def D5(self):
        return self._D5

    @property
    def D6(self):
        return self._D6

    @property
    def D7(self):
        return self._D7

    @property
    def D8(self):
        return self._D8

    @property
    def SDD3(self):
        return self._SDD3

    @property
    def SDD2(self):
        return self._SDD2


class wifi:
    def __init__(self, ssid=None, password=None):
        """
        初始化 WIFI 模組
        ssid: WIFI 名稱
        password: WIFI 密碼
        """
        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self.ssid = ssid
        self.password = password
        self.ap_active = False
        self.sta_active = False
        self.ip = None

    def setup(self, ap_active=False, sta_active=False):
        """
        設定WIFI模組
        ap_active: 是否啟用AP模式
        sta_active: 是否啟用STA模式
        使用方法:
        wi.setup(ap_active = True|False, sta_active = True|False)
        ||是or,&&是and.在語意上|是or,可是寫程式時要是||
        """
        self.ap_active = ap_active
        self.sta_active = sta_active
        self.ap.active(self.ap_active)
        self.sta.active(self.sta_active)

    def scan(self):
        """
        搜尋 WIFI
        返回: WIFI 列表

        使用方法:
        wi.scan()
        """
        if self.sta_active:
            wifi_list = self.sta.scan()
            print("Scan result:")
            for i in range(len(wifi_list)):
                print(wifi_list[i][0])
        else:
            print("STA 模式未啟用")

    def connect(self, ssid=None, password=None) -> bool:
        """
        連接 WIFI
        ssid: WIFI 名稱
        password: WIFI 密碼

        使用方法:
        wi.connect("WIFI_NAME", "PASSWORD")
        或在初始化時有設定過就可以不用再設定
        wi.connect()
        """
        ssid = ssid if ssid is not None else self.ssid
        password = password if password is not None else self.password

        if not self.sta_active:
            print("STA 模式未啟動")
            return False
        if ssid is None or password is None:
            print("SSID(WIFI名稱) 或密碼未設定")
            return False
        if self.sta_active:
            self.sta.connect(ssid, password)
            while not (self.sta.isconnected()):
                pass
            self.ip = self.sta.ifconfig()[0]  # 取得IP位址
            print("connect successfully", self.sta.ifconfig())
            return True


class LED:
    def __init__(self, r_pin, g_pin, b_pin, pwm: bool = False):
        """
        LED類別用於管理RGB LED

        屬性:
             RED(Pin):紅色LED。
             GREEN(Pin):綠色LED。
             BLUE(Pin):藍色LED。
        方法:
             __init__(r_pin, g_pin, b_pin, pwm=False):初始化LED。
             當 pwm=False 時，使用 Pin 控制 LED。
             當 pwm=True 時，使用 PWM 控制 LED。
             RED.value(value):設定紅色LED的狀態或亮度。
             GREEN.value(value):設定綠色LED的狀態或亮度。
             BLUE.value(value):設定藍色LED的狀態或亮度。
             RED.duty(duty):設定紅色LED的PWM佔空比(僅當 pwm=True 時可用)。
             GREEN.duty(duty):設定綠色LED的PWM佔空比(僅當 pwm=True 時可用)。
             BLUE.duty(duty):設定藍色LED的PWM佔空比( 僅當 pwm=True 時可用)。
        """

        # 因為LED還沒被創造出來所以先用self來儲存參數，等到創造出來後再用LED的屬性來儲存
        # 這樣才能在LED物件當中的其他指令使用這些變數
        # 例如: self.RED = Pin(r_pin, Pin.OUT)，這樣才能在其他方法使用self.RED來控制紅色LED
        # __init__是初始化，也就是要求使用LED這個物件的時候要提供的傳入參數
        # 例如: led = LED(r_pin=5, g_pin=6, b_pin=7, pwm=False)
        self.pwm = pwm
        if pwm == False:
            self.RED = Pin(r_pin, Pin.OUT)
            self.GREEN = Pin(g_pin, Pin.OUT)
            self.BLUE = Pin(b_pin, Pin.OUT)
        else:
            frequency = 1000  # 設定 PWM 頻率為 1000Hz
            duty_cycle = 0
            self.RED = PWM(Pin(r_pin), freq=frequency, duty=duty_cycle)
            self.GREEN = PWM(Pin(g_pin), freq=frequency, duty=duty_cycle)
            self.BLUE = PWM(Pin(b_pin), freq=frequency, duty=duty_cycle)

    def LED_open(self, RED_value, GREEN_value, BLUE_value):
        """
        LED開啟方法
        LED_open(RED_value, GREEN_value, BLUE_value)
        例如:
        led = LED(r_pin=5, g_pin=6, b_pin=7, pwm=False)
        led.LED_open(1, 0, 0)  # 開啟RED_LED, 關閉GREEN_LED和BLUE_LED

        led = LED(r_pin=5, g_pin=6, b_pin=7, pwm=True)
        led.LED_open(512, 0, 0)  # 設定RED_LED亮度為512, 關閉GREEN_LED和BLUE_LED
        """
        if self.pwm == False:
            self.RED.value(RED_value)
            self.GREEN.value(GREEN_value)
            self.BLUE.value(BLUE_value)
        else:
            self.RED.duty(RED_value)
            self.GREEN.duty(GREEN_value)
            self.BLUE.duty(BLUE_value)


class MQTT:
    def __init__(self, client_id, server, user, password, keepalive):
        # 創建MQTT客戶端並連接到服務器。
        # server (str):Server網址。
        # user (str):帳號。
        # password (str):密碼。
        # keepalive (int):保持連線時間。
        self.mqtt_client = MQTTClient(
            client_id, server, user=user, password=password, keepalive=keepalive
        )

    def connect(self):
        # 連接到MQTT服務器。
        try:
            self.mqtt_client.connect()
        except:
            sys.exit()
        finally:
            print("connected MQTT server")

    def subscribe(self, topic: str, callback: function):
        # 訂閱主題並設置回調函數。
        # topic (str):主題名稱。
        # callback (function):接收訊息時調用的函數。
        self.mqtt_client.set_callback(callback)
        self.mqtt_client.subscribe(topic)

    def check_msg(self):
        # 檢查是否有新訊息並調用回調函數。
        self.mqtt_client.check_msg()
        self.mqtt_client.ping()
