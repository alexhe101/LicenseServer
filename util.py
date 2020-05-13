import json
import uuid


def read_json(filename):
    with open(filename) as file_object:
        data = json.load(file_object)
    return data


def write_json(filename, data):
    with open(filename, 'w') as file_object:
        json.dump(data, file_object)


def narrate(title, req, client):
    print(f'SERVER: {title}, {req}, {client}')


def gen_id():
    return uuid.uuid4().hex
