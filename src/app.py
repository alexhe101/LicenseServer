from requests import get
from json import loads
from flask import Flask, render_template, request, redirect
from datetime import datetime
app = Flask(__name__)


def get_db():
    db = loads(get('http://127.0.0.1:10002/db').text)
    for k in db.keys():
        for u in db[k]['uid'].keys():
            db[k]['uid'][u] = str(datetime.fromtimestamp(db[k]['uid'][u]))
    return db


def delete(ku):
    get('http://127.0.0.1:10002/del/'+ku)


def gen_key(max):
    return get('http://127.0.0.1:10002/gen/'+max).txt


@app.route('/', methods=['GET', 'POST'])
def index():
    key = ''
    if request.method == 'POST':
        if 'gen' in list(request.form.keys()):
            key = gen_key(request.form.get('max'))
        else:
            delete(list(request.form.keys())[0])
    return render_template('index.html', db=get_db(), key=key)


if __name__ == '__main__':
    app.run()
