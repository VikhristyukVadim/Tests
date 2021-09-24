import argparse

import requests

from server_app import add_item, get_list, change_note_by_id, delete_note, find_note_by_txt

parser = argparse.ArgumentParser(description='--> launch App')

parser.add_argument('--new_note', help='--> create new note(type the text in quotes)')
parser.add_argument('--note_list', action='store_true', help='--> load note list')
parser.add_argument('--change_by_id', nargs=2, help='--> transform note (specify first id then text )')
parser.add_argument('--find_note_by_txt', help='--> transform note ( text )')
parser.add_argument('--delete_note', help='--> delete note by id')

args = parser.parse_args()


def result(q):
    if q.new_note:
        res = requests.post("http://127.0.0.1:5000/example/new_txt", json={'data': q.new_note})
        if res:
            print('Response OK',res.json())
        else:
            print('Response Failed')
    elif q.note_list:
        res = requests.get("http://127.0.0.1:5000/example/list").json()
        if res:
            print('Response OK',res)
        else:
            print('Response Failed')
    elif q.change_by_id:
        requests.put("http://127.0.0.1:5000/example/change/" + str(q.change_by_id[0]), json={'data': q.change_by_id[1]})
    elif q.find_note_by_txt:
        requests.get("http://127.0.0.1:5000/example/find/" + q.find_note_by_txt)
    elif q.delete_note:
        requests.delete("http://127.0.0.1:5000/example/delete/" + str(q.change_by_id[0]))


result(args)
