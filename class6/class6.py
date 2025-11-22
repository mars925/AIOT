#########################匯入模組#########################
import socket

#########################宣告與設定#########################
HOST = "localhost"  # IP
PORT = 5438  # Port
server_socket = socket.socket()  # 建立socket
server_socket.bind((HOST, PORT))  # 綁定IP和Port
server_socket.listen(5)  # 最大連接數量，超過則拒絕連接
print("server:{} port:{} start".format(HOST, PORT))  # 顯示伺服器IP和Port
client, addr = server_socket.accept()  # 接受客戶端連接，返回客戶端socket和地址
print("client address:{}, port:{}".format(addr[0], addr[1]))

#########################主程式#########################
while True:
    msg = client.recv(128).decode(
        "utf8"
    )  # 接收客戶端訊息，100為接收訊息的最大長度，utf8為解碼方式
    print("Receive Message:" + msg)
    reply = ""  # 建立伺服器回應字串

    if msg == "Hi":
        reply = "Hello!"  # 將字串轉換為位元組，因為socket只能傳送位元組
        client.send(reply.encode("utf8"))
    elif msg == "Bye":
        client.send(b"quit")
        break
    else:
        reply = "what??"
        client.send(reply.encode("utf8"))

client.close()  # 關閉與客戶端溝通
server_socket.close()  # 關閉伺服器
