#########################匯入模組#########################
import paho.mqtt.client as mqtt


#########################函式與類別定義#########################
def on_connect(client, userdata, connect_flags, reason_code, properties):
    """
    當客戶端成功連接到代理伺服器時調用的回調函數。

    參數：
    - client：此回調函數的客戶端實例。
    - userdata：在客戶端構造函數中設置的私有用戶數據，或使用`user_data_set()`設置的數據。
    - connect_flags：連接標誌。
    - reason_code：連接結果。
    - properties：在CONNACK封包中返回的屬性。

    返回值：
    無
    """
    print(f"連線結果:{reason_code}")
    client.subscribe("沒出息")  # 訂閱主題


def on_message(client, userdata, msg):
    """
    當收到訊息時調用的回調函數。

    參數：
        client (mqtt.Client)：MQTT客戶端實例。
        userdata：在MQTT客戶端中設置的私有用戶數據。
        msg (mqtt.MQTTMessage)：收到的訊息。

    返回值：
        無
    """
    print(f"我訂閱的主題是:{msg.topic}, 收到訊息:{msg.payload.decode('utf-8')}")


#########################宣告與設定#########################
# 建立客戶端實例
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# 設定連接成功後的回調函數
client.on_connect = on_connect
# 設定接收訊息後的回調函數
client.on_message = on_message
# 設定使用者名稱和密碼
client.username_pw_set("singular", "Singular#1234")
# 連接伺服器
client.connect("mqtt.singularinnovation-ai.com", 1883, 60)
# client.connect("192.168.68.114", 1883, 60)
# 保持連線
client.loop_forever()
