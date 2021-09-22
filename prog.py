import argparse

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
        add_item(q.new_note)
    elif q.note_list:
        get_list()
    elif q.change_by_id:
        change_note_by_id(q.change_by_id)
    elif q.find_note_by_txt:
        find_note_by_txt(q.find_note_by_txt)
    elif q.delete_note:
        delete_note(int(q.delete_note))


result(args)
