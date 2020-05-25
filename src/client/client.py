from os.path import isfile
import socket
import os
import schedule

from util import gen_id, read_json, read_text, write_text

config_path = 'config.json'
key_path = os.path.join(os.path.dirname(__file__),'key')
uid_path = os.path.join(os.path.dirname(__file__),'uid')
status_path = os.path.join(os.path.dirname(__file__),"status.txt")

sock = None
ip = ''
port = 0

conf = {}
key = ''
uid = ''
status_file = None
activated = False


def main():
    try:
        global conf, uid, key, ip, port, sock,status_file
        conf = read_json(os.path.join(os.path.dirname(__file__),config_path))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setdefaulttimeout(3)
        sock.settimeout(3)
        status_file = open(status_path, "w")
        #sock.setblocking(False)
        ip = conf['remote']
        port = conf['remote_port']

        if isfile(key_path):
            key = read_text(key_path)
        else:
            prompt_for_key()

        if isfile(uid_path):
            uid = read_text(uid_path)
        else:
            uid = gen_id()
            write_text(uid_path, uid)

        check_alive()
        #schedule.every(conf['interval']).seconds.do(check_alive)
        schedule.every(5).seconds.do(check_alive)
        print("client is running")
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        print('manual exit')
        post_request("GBYE")
        sock.close()


def check_alive():
    res = post_request('HELO')
    status_file = open(status_path, "w")
    if res == 'NKEY':
        prompt_for_key()
    elif res == 'FULL':
        print('full')
    elif res == 'GOOD':
        print('good')
    elif res == 'NCMD':
        print('NCMD')
    else:
        res = "remote disconnected"
        print(res)
    status_file.write(res)
    status_file.close()


def post_request(req):
    req = '.'.join([req, key, uid]).encode('ascii')
    sock.sendto(req, (ip, port))
    try:
        res = sock.recv(4).decode('ascii')
    except socket.timeout:
        res = ("DISC")
    except ConnectionError:
        res = ("DISC")
    return res


def prompt_for_key():
    global key
    res = 'NKEY'
    status_file = open(status_path, "w")
    while res == 'NKEY':
        #while len(key) != 32:
        status_file.write('Please enter valid license key: ')
        key = input('Please enter valid license key: ')
        res = post_request('HELO')
    write_text(key_path, key)
    status_file.close()


if __name__ == '__main__':
    main()
