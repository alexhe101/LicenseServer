import socket
import uuid
from sys import argv
import schedule

id = ""
key = ""
ip = ""
port = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
''' 初始化本机信息'''


def init():
    global id
    global ip
    global port
    global sock
    f = open("uuid.id", 'w+')
    id = f.read()
    if id == "":
        id = uuid.uuid1()
        f.write(str(id))
    f.close()
    ip = argv[1]
    port = eval(argv[2])


def narrate(msg):
    print("Server response:" + msg)


def postRequest(req):
    data = req + " " + str(id) + "." + key
    ret = sock.sendto(data.encode('utf-8'), (ip, port))
    while ret == -1:
        ret = sock.sendto(data.encode('utf-8'), (ip, port))
    recvMsg = sock.recv(1024).decode('utf-8')
    if recvMsg[:4] == "FAIL":
        narrate(recvMsg)
        if req == "VALD":
            exit(0)
        else:
            return False
    elif recvMsg[:4] == "TICK":
        narrate(recvMsg)
        return True
    elif recvMsg[:4] == "THNX":
        narrate(recvMsg)
        return True
    elif recvMsg[:4] == "GOOD":
        return True
    else:
        narrate("error msg")
        if req == "VALD":
            exit(0)
        else:
            return False


def main():
    init()
    if not postRequest("HELO"):  # 激活本机
        print("activate failed")
    schedule.every(2).minutes.do(postRequest,"VALD")

    try:
        print("client is running")
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        print('manual exit')
    postRequest("GBYE")
    sock.close()


if __name__ == '__main__':
    main()
