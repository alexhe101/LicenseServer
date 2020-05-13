# -*- coding: utf-8 -*-
import socket
import signal
import os
import errno
import json
import uuid
import time
import schedule
# 票据数据存储
ticket_database = 'key.json'
key = {}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 程序配置存储
        app_config = 'config.json'

        # 读取程序配置
        conf = read_data(app_config)
        server = conf["server"]
        port = conf["port"]

        # 预处理读取数据文件
        global key
        key = read_data(ticket_database)

        # 绑定服务器本机
        sock.bind((server, port))

        # 服务器每5s尝试回收票据
        #signal.signal(signal.SIGALRM, ticket_reclaim)
        #signal.alarm(5)
        schedule.every(1).minutes.do(ticket_reclaim)

        while True:
            try:
                print('wait for datagram......')
                data, addr = sock.recvfrom(1024)
                data = data.decode('utf-8')
                print(f'accept new datagram from {addr}')
                narrate('GOT', data, addr)
                #time_left = signal.alarm(0)  # 正常操作中关闭alarm
                handle_request(data, addr, sock)
                #signal.alarm(time_left)
                schedule.run_pending()
            except ConnectionResetError:
                print("connection reset")
    except KeyboardInterrupt:
        print('manual exit')
    sock.close()


# 处理请求
def handle_request(req, client, sock):
    if req[0:4] == 'HELO':
        response = do_hello(req[5:].split('.'))
    elif req[0:4] == 'GBYE':
        response = do_goodbye(req[5:].split('.'))
    elif req[0:4] == 'VALD':
        response = do_validate(req[5:].split('.'))
    else:
        response = 'FAIL invalid request'
    narrate("SAID:", req, client)
    ret = sock.sendto(response.encode('utf-8'), client)
    if ret == -1:
        print("SERVER sendto failed")

# 处理HELO命令
def do_hello(para):
    remote_key = para[0]
    remote_uid = para[1]
    if remote_key not in key.keys():
        return 'FAIL invalid key'

    if len(key[remote_key]['uid']) >= key[remote_key]['max']:
        return 'FAIL no ticket available'

    key[remote_key]['uid'][remote_uid] = time.time()
    write_data(ticket_database, key)
    return 'TICK'


# 处理GBYE命令
def do_goodbye(para):
    remote_key = para[0]
    remote_uid = para[1]

    # bad ticket
    if remote_key not in key.keys():
        narrate('Bogus key ', (remote_key, remote_uid), None)
        return 'FAIL invalid key'

    if remote_uid not in key[remote_key]['uid'].keys():
        narrate('Bogus ticket', (remote_key, remote_uid), None)
        return 'FAIL invalid ticket'

    # good ticket
    key[remote_key]['uid'].pop(remote_uid)
    write_data(ticket_database, key)
    return 'THNX seeya!'


# 进行票据验证
def do_validate(para):
    remote_key = para[0]
    remote_uid = para[1]

    # bad ticket
    if remote_key not in key.keys():
        narrate('Bogus key ', (remote_key, remote_uid), None)
        return 'FAIL invalid key'

    if remote_uid not in key[remote_key]['uid'].keys():
        narrate('Bogus ticket', (remote_key, remote_uid), None)
        return 'FAIL invalid ticket'

    # good ticket
    key[remote_key]['uid'][remote_uid] = time.time()
    write_data(ticket_database, key)
    return 'GOOD valid ticket'


# 处理服务器返回的叙述
def narrate(title, req, client):
    print(f'SERVER: {title}, {req}, {client}')


# 收回丢失的票据
def ticket_reclaim():
    t = time.time()
    for k in key.keys():
        for i in list(key[k]['uid'].keys()):
            if t - key[k]['uid'][i] >= 5*60:
                key[k]['uid'].pop(i)
                narrate("freeing ", i, None)
                write_data(ticket_database, key)
    # reset alarm clock
    #signal.alarm(5)


# 读取数据
def read_data(filename):
    with open(filename) as file_object:
        data = json.load(file_object)
    return data


# 存储数据
def write_data(filename, data):
    with open(filename, 'w') as file_object:
        json.dump(data, file_object)


if __name__ == '__main__':
    main()
