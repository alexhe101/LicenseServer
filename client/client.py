import socket
import uuid
import signal
from sys import argv
id = ""
key = ""
MSGLEN = 128
ip = ""
port = 0
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
''' 初始化本机信息'''
def init():
    global id
    global ip
    global port
    global sock
    f = open("uuid.id")
    id = f.read()
    if id=="":
        id = uuid.uuid1()
        f.write(id)
    f.close()
    ip = argv[1]
    port = eval(argv[2])

def narrate(msg):
    print("Server response:"+msg)

def postRequest(req):
    data = req+" "+id+"."+key
    ret = sock.sendto(data.encode('utf-8'), (ip, port))
    while ret==-1:
        ret = sock.sendto(data.encode('utf-8'), (ip, port))
    recvMsg = sock.recv(1024).decode('utf-8')
    if recvMsg[:4]=="FAIL":
        narrate(recvMsg)
        if req=="VALD":
            exit(0)
        else:
            return False
    elif recvMsg[:4]=="TICK":
        narrate(recvMsg)
        return True
    elif recvMsg[:4]=="THNX":
        narrate(recvMsg)
        return True
    elif recvMsg[:4]=="GOOD":
        signal.alarm(200)
        return True
    else:
        narrate("error msg")
        if req=="VALD":
            exit(0)
        else:
            return False


def main():
    init()
    if postRequest("HELO")!=True: #激活本机
        print("activate failed")
    signal.signal(signal.SIGALRM, postRequest("VALD"))
    signal.alarm(200)
    try:
        print("client is runing")
        while True:
            pass
    except KeyboardInterrupt:
            print('manual exit')
    postRequest("GBYE")
    sock.close()
if __name__ == '__main__':
    main()












