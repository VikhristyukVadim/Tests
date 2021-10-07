import argparse

import requests
from methods import check_status

from urllib.parse import unquote

parser = argparse.ArgumentParser(description='--> launch App', formatter_class=argparse.RawTextHelpFormatter, )

serverWay = 'http://127.0.0.1:5000'

parser.add_argument('--server', help=serverWay, nargs="*")

parser.add_argument('--new_note', nargs="*", help='--> create new note')
parser.add_argument('--note_list', action='store_true', help='--> load note list')
parser.add_argument('--change_by_id', nargs=2, help='--> transform note (specify first id then text )')
parser.add_argument('--find_note_by_txt', help='--> transform note ( text )')
parser.add_argument('--delete_note', help='--> delete note by id')

parser.add_argument('--add_category', '--add_c', help='--> add new category', nargs="*")
parser.add_argument('--category_list', '--list_c', action='store_true', help='--> load category list')
parser.add_argument('--del_category', '--del_c', help='--> delete category by name')
parser.add_argument('--edit_category', '--edit_c', nargs=2, help='--> edit category')
parser.add_argument('--find_n_in_category', '--find_n', help='--> find notes in category ( int )')
parser.add_argument('--del_n_in_category', '--del_in_c', help='--> delete notes in category')
parser.add_argument('--change_n_category', '--ch_c', nargs=2,
                    help='--> change notes category ( first note int, second category int )')

args = parser.parse_args()


def result(q):
    server_url = q.server[0]
    try:
        if q.server:
            # ------------------------------------------------------------------------------------------------------
            # NOTES
            # ------------------------------------------------------------------------------------------------------
            if q.new_note:
                to_str = ' '.join(q.new_note)
                to_split = to_str.split('...')
                check_status(requests.post(server_url + "/new_txt/" + unquote(str(to_split[1])),
                                           json={'data': to_split[0]}))
            elif q.note_list:
                check_status(requests.get(server_url + "/list"))
            elif q.change_by_id:
                check_status(requests.put(server_url + "/change/" + unquote(str(q.change_by_id[0])),
                                          json={'data': q.change_by_id[1]}))
            elif q.find_note_by_txt:
                check_status(requests.get(server_url + "/find/" + unquote(q.find_note_by_txt)))
            elif q.delete_note:
                check_status(requests.delete(server_url + "/delete/" + unquote(str(q.delete_note))))
            # ------------------------------------------------------------------------------------------------------
            # CATEGORY
            # ------------------------------------------------------------------------------------------------------
            elif q.add_category:
                to_str = ' '.join(q.add_category)
                check_status(requests.post(server_url + "/c_add", json={'data': to_str}))
            elif q.category_list:
                check_status(requests.get(server_url + "/c_list"))
            elif q.edit_category:
                check_status(requests.put(server_url + "/c_edit/" + unquote(str(q.edit_category[0])),
                                          json={'data': q.edit_category[1]}))
            elif q.del_category:
                check_status(requests.delete(server_url + "/c_del/" + unquote(str(q.del_category))))
            elif q.find_n_in_category:
                check_status(requests.get(server_url + "/find_n/" + unquote(q.find_n_in_category)))
            elif q.del_n_in_category:
                check_status(requests.delete(server_url + "/del_n_in_cat/" + unquote(str(q.del_n_in_category))))
            elif q.change_n_category:
                check_status(
                    requests.put(server_url + "/ch_n_cat", json={'data': q.change_n_category}))
    except requests.exceptions.ConnectionError as error:
        print(str(error))


result(args)
