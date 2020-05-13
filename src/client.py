from os.path import isfile
import socket
from sys import argv

import schedule

from util import gen_id, read_json, read_text, write_text

config_path = 'sample/client/config.json'
key_path = 'key'
uid_path = 'uid'

sock = None
ip = ''
port = 0

conf = {}
key = ''
uid = ''

activated = False


def main():
    try:
        global conf, uid, key, ip, port, sock
        conf = read_json(config_path)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = conf['remote']
        port = conf['remote_port']

        if isfile(key_path):
            key = read_text(key)
        else:
            prompt_for_key()

        if isfile(uid_path):
            uid = read_text(key_path)
        else:
            uid = gen_id()
            write_text(uid_path, uid)

        check_alive()
        schedule.every(conf['interval']).seconds.do(check_alive)

        print("client is running")
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        print('manual exit')
        post_request("GBYE")
        sock.close()


def check_alive():
    res = post_request('HELO')
    if res == 'NKEY':
        prompt_for_key()
    elif res == 'FULL':
        print('full')
    elif res == 'GOOD':
        print('good')
    elif res == 'NCMD':
        print('NCMD')


def post_request(req):
    req = '.'.join([req, key, uid]).encode('ascii')
    while sock.sendto(req, (ip, port)) == -1:
        pass
    res = sock.recv(4).decode('ascii')
    return res


def prompt_for_key():
    global key
    res = 'NKEY'
    while res == 'NKEY':
        while len(key) != 32:
            key = input('Please enter valid license key: ')
        res = post_request('HELO')
    write_text(key_path, key)


if __name__ == '__main__':
    main()
