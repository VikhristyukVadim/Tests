import argparse

import requests
from requests.exceptions import HTTPError

parser = argparse.ArgumentParser(description='--> launch App', formatter_class=argparse.RawTextHelpFormatter, )

parser.add_argument('--new_note', help='--> create new note(type the text in quotes', nargs="*")
parser.add_argument('--note_list', action='store_true', help='--> load note list')
parser.add_argument('--change_by_id', nargs=2, help='--> transform note (specify first id then text )')
parser.add_argument('--find_note_by_txt', help='--> transform note ( text )')
parser.add_argument('--delete_note', help='--> delete note by id')

args = parser.parse_args()


def check_status(res):
    try:
        response = res
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Response OK', response.text)


def result(q):
    if q.new_note:
        to_str = ' '.join(q.new_note)
        check_status(requests.post("http://127.0.0.1:5000/example/new_txt", json={'data': to_str}))
    elif q.note_list:
        check_status(requests.get("http://127.0.0.1:5000/example/list"))
    elif q.change_by_id:
        check_status(requests.put("http://127.0.0.1:5000/example/change/" + str(q.change_by_id[0]),
                                  json={'data': q.change_by_id[1]}))
    elif q.find_note_by_txt:
        check_status(requests.get("http://127.0.0.1:5000/example/find/" + q.find_note_by_txt))
    elif q.delete_note:
        check_status(requests.delete("http://127.0.0.1:5000/example/delete/" + str(q.delete_note)))


result(args)
