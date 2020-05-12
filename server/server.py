# -*- coding: utf-8 -*-
import socket
import signal
import os
import errno


def main():
    try:
        # 默认绑定服务器本机10001端口
        s.bind(('0.0.0.0', 10001))

        # 服务器每5s尝试回收票据
        signal.signal(signal.SIGALRM, ticket_reclaim)
        signal.alarm(5)

        while True:
            try:
                print('\nwait for datagram......')
                data, addr = s.recvfrom(1024)
                print('accept new datagram from {}'.format(addr))
                narrate("GOT:", data.decode(), ('0.0.0.0', 10001))
                time_left = signal.alarm(0)  # 正常操作中关闭alarm
                handle_request(data, addr)
                signal.alarm(time_left)
            except ConnectionResetError:
                print("connection reset")
    except KeyboardInterrupt:
        print('manual exit')
    s.close()


# 处理请求
def handle_request(req, client):
    req = req.decode()
    if req[0:4] == 'HELO':
        response = do_hello(req)
    elif req[0:4] == 'GBYE':
        response = do_goodbye(req)
    elif req[0:4] == 'VALD':
        response = do_validate(req)
    else:
        response = 'FAIL invalid request'
    narrate("SAID:", req, client)
    ret = s.sendto(response.encode(encoding='utf-8'), client)
    if ret == -1:
        print("SERVER sendto failed")


# 处理HELO命令
def do_hello(req):
    global num_tickets_out
    x = 0
    if num_tickets_out >= MAXUSERS:
        return 'FAIL no tickets available'

    # find the sequence of avail_ticket
    for ticket in ticket_array:
        if ticket == TICKET_AVAIL:
            break
        x += 1

    # A sanity check - should never happen
    if x == MAXUSERS:
        narrate("database corrupt", "", None)
        return 'FAIL database corrupt'

    # generate ticket of form: pid.slot
    ticket_array[x] = int(req[5:])
    write_data(ticket_database)
    replybuf = 'TICK {}.{}'.format(req[5:], str(x))
    num_tickets_out += 1
    return replybuf


# 处理GBYE命令
def do_goodbye(req):
    try:
        index = req.index('.')
        pid = req[5:index]
        slot = req[index + 1:]
        if (int(slot) >= num_tickets_out) or (ticket_array[int(slot)] != pid):
            raise ValueError
    except ValueError:
        return 'FAIL invalid ticket'
    ticket_array[int(slot)] = TICKET_AVAIL
    write_data(ticket_database)
    return 'THNX See ya!'


# 进行票据验证
def do_validate(req):
    try:
        index = req.index('.')
        pid = req[5:index]
        slot = req[index + 1:]
        if (int(slot) >= num_tickets_out) or (ticket_array[int(slot)] != pid):
            raise ValueError
    # bad ticket
    except ValueError:
        narrate('Bogus ticket ', req[5:], None)
        return 'FAIL invalid ticket'
    # good ticket
    return 'GOOD Valid ticket'


# 处理服务器返回的叙述
def narrate(title, req, client):
    response = 'SERVER:{}{} {}'.format(title, req, client)
    print(response)


# 收回丢失的票据
def ticket_reclaim(signum, frame):
    global num_tickets_out
    for i in range(0, MAXUSERS):
        if ticket_array[i] != TICKET_AVAIL:
            try:
                os.kill(ticket_array[i], 0)
            except OSError as e:
                if e.errno == errno.ESRCH:
                    tick = '{}.{}'.format(ticket_array[i], i)
                    narrate("freeing ", tick, None)
                    ticket_array[i] = TICKET_AVAIL
                    write_data(ticket_database)  # 即时更新数据表
                    num_tickets_out -= 1
    # reset alarm clock
    signal.alarm(5)


# 读取数据
def read_data(filename):
    i = 0
    with open(filename) as file_object:
        for line in file_object:
            ticket_array[i] = int(line)
            i += 1


# 存储数据
def write_data(filename):
    with open(filename, 'w') as file_object:
        for ticket in ticket_array:
            file_object.write(str(ticket) + '\n')


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 票据数据存储
    ticket_database = 'tickets.txt'

    # 暂定最大用户数量1000
    MAXUSERS = 1000

    # 票据列表
    ticket_array = [0] * MAXUSERS

    # 可用于分配的票据标记
    TICKET_AVAIL = 0

    # 已经分配的票据数量
    num_tickets_out = 0

    # 预处理读取数据文件
    read_data(ticket_database)

    main()
