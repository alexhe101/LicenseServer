import socket
from pathlib import Path
from threading import Thread

import schedule
from flask import Flask

from database import database
from util import narrate, read_json

api = Flask(__name__)


def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((conf['server'], conf['port']))
        narrate('server', 'listen at', f"{conf['server']}:{conf['port']}")
        schedule.every(conf['refresh']).seconds.do(db.reclain)
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
    if op == 'GBYE':
        return do_goodbye(key, uid)
    return 'NCMD'


def do_hello(key, uid):
    if not db.has_key(key):
        return 'NKEY'
    if db.full(key) and not db.has_uid(key, uid):
        inactive = db.get_inactive(key)
        if not inactive:
            return 'FULL'
        db.del_uid(key, inactive)
    db.update_uid(key, uid)
    return 'GOOD'


def do_goodbye(key, uid):
    db.del_uid(key, uid)
    return 'THNX'


@api.route('/<op>')
@api.route('/<op>/<int:max>')
@api.route('/<op>/<string:key>')
@api.route('/<op>/<string:key>/<string:uid>')
def do(op, key='', uid='', max=0):
    res, code = '', 200
    if op == 'db':
        res = db.db
    if op == 'gen_key':
        res = db.gen_key(max)
    if op == 'del_key':
        db.del_key(key)
    if op == 'del_uid':
        db.del_uid(key, uid)
    return res, code


if __name__ == '__main__':
    global conf, db
    conf = read_json(Path(__file__).parents[1].joinpath(
        'sample', 'server', 'config.json'))
    db = database(Path(__file__).parents[1].joinpath(
        'sample', 'server', 'key.json'))

    Thread(target=api.run, kwargs={
           'host': conf['api'], 'port': conf['api_port']}).start()

    main()
