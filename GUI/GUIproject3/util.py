import json
from uuid import uuid4


def read_text(file):
    with open(file) as f:
        data = f.read()
    return data


def write_text(file, data):
    with open(file, 'w') as f:
        f.write(data)


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def write_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)


def gen_id():
    return uuid4().hex


def narrate(subject, verb, object, level='info'):
    print(f'[{level}] {subject}: {verb} {object}')
