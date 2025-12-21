#########################匯入模組#########################
import network

#########################函式與類別定義#########################

#########################宣告與設定#########################
wlan = network.WLAN(network.STA_IF)  # 建立 WLAN 物件，設定為接收模式
ap = network.WLAN(network.AP_IF)  # 建立 WLAN 物件，設定為熱點模式
ap.active(False)
wlan.active(True)
# 啟用存取點模式
wifi_list = wlan.scan()  # 掃描附近的無線網路
print("scan result:")
for i in range(len(wifi_list)):
    print(wifi_list[i])

wlssId = "Singular_AI"
wlPwd = "Singular#1234"
wlan.connect(wlssId, wlPwd)  # 連接到指定的無線網路
while not wlan.isconnected():  # 等待連接成功
    pass
print("connet successfully")
#########################主程式#########################
