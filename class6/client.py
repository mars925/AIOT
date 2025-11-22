#########################匯入模組#########################
import socket

#########################宣告與設定#########################
client_socket = socket.socket()
client_socket.connect(("127.0.0.1", 5438))  # 連接到伺服器

#########################主程式#########################
while True:
    msg = input("Input Message:")  # 輸入想要傳送到伺服器的訊息
    client_socket.send(msg.encode("utf8"))  # 將訊息轉換為位元組後傳送到伺服器
    reply = client_socket.recv(128).decode("utf8")  # 接收伺服器回傳的訊息並解碼
    if reply == "quit":
        print("Disconnected")
        client_socket.close()
        break
    print(reply)