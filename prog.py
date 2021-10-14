import argparse

import requests
from methods import check_status, unite_txt

"""Initialising of arg parser"""
parser = argparse.ArgumentParser(description='--> launch App', formatter_class=argparse.RawTextHelpFormatter, )
subparsers = parser.add_subparsers(title="object", dest="object", help="parser_note help")

"""Default server"""
serverWay = 'http://127.0.0.1:5000'

"""Creating parser arguments"""
# Server parser-------------------------------------------------------------------------------------------------------
parser.add_argument('--server', help=serverWay, required=True)

# Note parsers -------------------------------------------------------------------------------------------------------
note_sub = subparsers.add_parser("note", help="note element")
note_actions = note_sub.add_subparsers(dest="action", help="actions for working with notes ", required=True)

# note actions---
note_add_sub = note_actions.add_parser("add", help="add new note")
note_txt_sub = note_add_sub.add_argument('--text', required=True, nargs="*", help="type text of note, use str")
note_category_sub = note_add_sub.add_argument('--category', required=True, help="insert ID of note category, use int")

note_list_sub = note_actions.add_parser("list")

note_change_text_sub = note_actions.add_parser("change_note", help="change note text")
note_id_change_sub = note_change_text_sub.add_argument('--id', type=int, required=True,
                                                       help="insert ID changed note, use int")
note_txt_change_sub = note_change_text_sub.add_argument('--text', nargs='*', required=True,
                                                        help="insert new text for note, use str")

note_change_category_sub = note_actions.add_parser("change_category",
                                                   help="change category of note use note ID and category ID")
note_category_change_category_sub = note_change_category_sub.add_argument('--id', required=True)
note_id_change_category_sub = note_change_category_sub.add_argument('--category_id', required=True)

note_find_sub = note_actions.add_parser("find", help="find note by text, use str")
note_id_find_sub = note_find_sub.add_argument('--text', required=True, help="insert text, use str")

note_del_sub = note_actions.add_parser("delete", help="delete note")
note_id_sub = note_del_sub.add_argument('--id', required=True, help="insert ID deleted note, use int")

# range_choice = [id_change_sub.dest, txt_change_sub.dest, category_change_sub.dest]
# choice_change_sub = change_sub.add_argument('ch', choices=range_choice)


# Category parsers----------------------------------------------------------------------------------------------------

category_sub = subparsers.add_parser("category", help="parser_category help")
category_actions = category_sub.add_subparsers(dest="action", help="action help", required=True)

# category actions---
category_add_sub = category_actions.add_parser("add")
category_txt_sub = category_add_sub.add_argument('--text', nargs="*", required=True)

category_list_sub = category_actions.add_parser("list")

category_change_text_sub = category_actions.add_parser("change_name")
category_id_change_sub = category_change_text_sub.add_argument('--id', type=int, required=True)
category_txt_change_sub = category_change_text_sub.add_argument('--text', nargs="*", required=True)

category_find_sub = category_actions.add_parser("find")
category_id_find_sub = category_find_sub.add_argument('--id', required=True)

category_clear_notes_sub = category_actions.add_parser("clear")
category_id_clear_notes_sub = category_clear_notes_sub.add_argument('--id', required=True)

category_del_sub = category_actions.add_parser("delete")
category_id_sub = category_del_sub.add_argument('--id', required=True)

args = parser.parse_args()


# Processing requests
def result(res):
    # Define server URL
    server_url = res.server

    # Using an error handler
    try:
        # If the correct server is available, we continue to form the request.
        if res.server:
            # NOTES___________________________________________________________________________________________________
            if res.object == "note":
                if res.action == "add":
                    check_status(requests.post(server_url + "/add_note",
                                               json={"quote": unite_txt(res.text),
                                                     "category": int(res.category)}))

                elif res.action == "list":
                    check_status(requests.get(server_url + "/list_notes"))

                elif res.action == "change_note":
                    check_status(requests.put(server_url + "/change_note",
                                              json={'id': res.id,
                                                    "quote": unite_txt(res.text)}))

                elif res.action == "change_category" and res.category_id is not None:
                    check_status(requests.put(server_url + "/change_category",
                                              json={"id": int(res.id),
                                                    "category_id": int(res.category_id)}))

                elif res.action == "find":
                    check_status(requests.get(server_url + "/find_note",
                                              json={"quote": unite_txt(res.text)}))

                elif res.action == "delete":
                    check_status(requests.delete(server_url + "/delete_note",
                                                 json={"id": int(res.id)}))

            # CATEGORY________________________________________________________________________________________________
            elif res.object == "category":

                if res.action == "add":
                    check_status(requests.post(server_url + "/add_category",
                                               json={'quote': unite_txt(res.text)}))

                elif res.action == 'list':
                    check_status(requests.get(server_url + "/list_category"))

                elif res.action == 'change_name':
                    check_status(requests.put(server_url + "/change_name",
                                              json={"id": res.id, "quote": unite_txt(res.text)}))

                elif res.action == 'clear':
                    check_status(requests.delete(server_url + "/clear",
                                                 json={"id": res.id}))

                elif res.action == 'find':
                    check_status(requests.get(server_url + "/find_category_note",
                                              json={"id": res.id}))

                elif res.action == 'delete':
                    check_status(requests.delete(server_url + "/delete_category",
                                                 json={"id": res.id}))

    except requests.exceptions.ConnectionError as error:
        print(str(error))


result(args)
