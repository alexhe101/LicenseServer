import socket


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
    response = narrate("SAID:", response, client)
    ret = s.sendto(response.encode(encoding='utf-8'), client)
    if ret == -1:
        print("SERVER sendto failed")


# 处理HELO命令
def do_hello(req):
    global num_tickets_out
    x = 0
    if len(ticket_array) >= MAXUSERS:
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
    ticket_array.append(req[5:])
    replybuf = 'TICK {}.{}'.format(req[5:], str(x))
    num_tickets_out += 1
    return replybuf


# 处理GBYE命令
def do_goodbye(req):
    try:
        index = req.index('.')
        pid = req[5:index]
        slot = req[index+1:]
        if (int(slot) >= num_tickets_out) or (ticket_array[int(slot)] != pid):
            raise ValueError
    except ValueError:
        return 'FAIL invalid ticket'
    return 'THNX See ya!'


# 进行票据验证
def do_validate(req):
    try:
        index = req.index('.')
        pid = req[5:index]
        slot = req[index:]
        if (int(slot) >= num_tickets_out) or (ticket_array[int(slot)] != pid):
            raise ValueError
    # bad ticket
    except ValueError:
        narrate('Bogus ticket', req[5:], None)
        return 'FAIL invalid ticket'
    # good ticket
    return 'GOOD Valid ticket'


# 处理服务器返回的叙述
def narrate(title, response, client):
    response = 'SERVER:{}{} {}'.format(title, response, client)
    print(response)
    return response


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 默认绑定服务器本机10001端口
    s.bind(('0.0.0.0', 10001))
    # 票据列表
    ticket_array = []

    # 可用于分配的票据标记
    TICKET_AVAIL = 0

    # 已经分配的票据数量
    num_tickets_out = 0

    # 暂定最大用户数量1000
    MAXUSERS = 1000
    try:
        while True:
            print('\nwait for datagram......')
            data, addr = s.recvfrom(1024)
            print(f"accept new datagram from {addr}")
            handle_request(data, addr)
    except ConnectionResetError:
        print("Error")
    except KeyboardInterrupt:
        print('quiting')
    s.close()
