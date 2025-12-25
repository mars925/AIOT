#########################匯入模組#########################
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
# 搜尋 WIFI
wi.scan()
# 選擇要連接的WIFI
if wi.connect("Singular_AI", "Singular#1234"):
    print(f"IP={wi.ip}")
#########################主程式#########################

# 如果成功就會把ture存入if判斷中，且會回傳入使用者ip
# 如果失敗就會把False存入if判斷中
# if wi.connect("Singular_AI", "Singular#1234"):這行是在判斷是否連接成功
# 如果成功就會執行縮排內的程式碼
# print(f"IP={wi.ip}")這行是印出連接成功後的IP地址
