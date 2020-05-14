import socket
from pathlib import Path
from threading import Thread

import schedule
from flask import Flask

from database import database
from util import read_json, narrate

app = Flask(__name__)


def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((conf['server'], conf['port']))
        narrate('server', 'listen at', f"{conf['server']}:{conf['port']}")
        schedule.every(conf['refresh']).seconds.do(db.reclain_all)
        while True:
            try:
                req, addr = sock.recvfrom(70)
                req = req.decode('ascii')
                narrate(addr, 'request',  req)
                res = handle_request(req)
                sock.sendto(res.encode('ascii'), addr)
                narrate('server', 'respone', res)
                schedule.run_pending()
            except ConnectionResetError:
                narrate(addr, 'reset', 'connection', 'error')
    except KeyboardInterrupt:
        narrate('keyboard', 'interrupt', 'program', 'warning')
        sock.close()


def handle_request(req):
    op, key, uid = list(req.split('.'))
    if op == 'HELO':
        return do_hello(key, uid)
    elif op == 'GBYE':
        return do_goodbye(key, uid)
    else:
        return 'NCMD'


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


@app.route('/admin/gen_key')
def admin():
    key = db.gen_key()
    return key


if __name__ == '__main__':
    global conf, db
    conf = read_json(Path(__file__).parents[1].joinpath(
        'sample', 'server', 'config.json'))
    db = database(Path(__file__).parents[1].joinpath(
        'sample', 'server', 'key.json'))

    Thread(target=app.run, kwargs={
           'host': conf['api'], 'port': conf['api_port']}).start()

    main()
