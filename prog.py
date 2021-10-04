import argparse

import requests
from requests.exceptions import HTTPError, ConnectionError

from urllib.parse import unquote

parser = argparse.ArgumentParser(description='--> launch App', formatter_class=argparse.RawTextHelpFormatter, )

serverWay = 'http://127.0.0.1:5000'

parser.add_argument('--server', help=serverWay, nargs="*")

parser.add_argument('--new_note', help='--> create new note', nargs="*")
parser.add_argument('--note_list', action='store_true', help='--> load note list')
parser.add_argument('--change_by_id', nargs=2, help='--> transform note (specify first id then text )')
parser.add_argument('--find_note_by_txt', help='--> transform note ( text )')
parser.add_argument('--delete_note', help='--> delete note by id')

args = parser.parse_args()


def check_status(response):
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    except ConnectionError as bad_connect:
        print(f'Problem with connect: {bad_connect}')
    else:
        table_width = 50
        print('{:1} {:10}'.format('id', 'Note'.center(table_width, '_')))
        res = response.json()
        if res.get('data'):
            for i in res['data']:
                print("{:1} {:.50}".format(i['id'], i['quote'].ljust(table_width, ' ')))
        elif res.get('id'):
            print("{:1} {:.50}".format(res['id'], res['quote'].ljust(table_width, ' ')))
        elif res.get('message'):
            print(res['message'])
        else:
            print(res)


def result(q):
    server_url = q.server[0]
    try:
        if q.server:
            if q.new_note:
                to_str = ' '.join(q.new_note)
                check_status(requests.post(server_url + "/new_txt", json={'data': to_str}))
            elif q.note_list:
                check_status(requests.get(server_url + "/list"))
            elif q.change_by_id:
                check_status(requests.put(server_url + "/change/" + unquote(str(q.change_by_id[0])),
                                          json={'data': q.change_by_id[1]}))
            elif q.find_note_by_txt:
                check_status(requests.get(server_url + "/find/" + unquote(q.find_note_by_txt)))
            elif q.delete_note:
                check_status(requests.delete(server_url + "/delete/" + unquote(str(q.delete_note))))

    except requests.exceptions.ConnectionError as error:
        print(str(error))


result(args)
