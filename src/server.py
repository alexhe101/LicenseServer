import socket
from threading import Thread

import schedule
from flask import Flask

from database import database
from util import read_json, narrate

config_path = 'sample/server/config.json'
database_path = 'sample/server/key.json'

conf = {}
db = None
app = None


def init():
    global conf, db
    conf = read_json(config_path)
    db = database(database_path)


def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((conf['server'], conf['port']))
        schedule.every(conf['refresh']).seconds.do(db.reclain_all)

        while True:
            try:
                print('wait for datagram......')
                data, addr = sock.recvfrom(70)
                data = data.decode('ascii')
                print(f'accept new datagram from {addr}')
                narrate('GOT', data, addr)
                handle_request(data, addr, sock)
                schedule.run_pending()
            except ConnectionResetError:
                print("connection reset")
    except KeyboardInterrupt:
        print('manual exit')
        sock.close()


def handle_request(req, client, sock):
    op, key, uid = list(req.split('.'))
    if op == 'HELO':
        response = do_hello(key, uid)
    elif op == 'GBYE':
        response = do_goodbye(key, uid)
    else:
        response = 'NCMD'
    narrate("SAID:", req, client)
    ret = sock.sendto(response.encode('ascii'), client)
    if ret == -1:
        print("SERVER sendto failed")


def do_hello(key, uid):
    if not db.has_key(key):
        return 'NKEY'
    elif db.full(key) and not db.squeeze(key, conf['time_out']):
        return 'FULL'
    else:
        db.add_uid(key, uid)
        return 'GOOD'


def do_goodbye(key, uid):
    db.del_uid(key, uid)
    return 'GOOD'


def api():
    global app
    app = Flask(__name__)
    app.run(host=conf['control'], port=conf['control_port'])


if __name__ == '__main__':
    init()
    Thread(target=api).run()
    main()
