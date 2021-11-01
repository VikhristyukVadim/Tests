import argparse


def argument_parser(server_way):
    """Initialising of arg parser"""
    parser = argparse.ArgumentParser(description='--> launch App', formatter_class=argparse.RawTextHelpFormatter, )
    subparsers = parser.add_subparsers(title="object", dest="object", help="parser_note help")

    """Creating parser arguments"""
    # Server parser----------------------------------------------------------------------------------------------------
    parser.add_argument('--server', help=server_way, required=True)

    # NOTE parsers ----------------------------------------------------------------------------------------------------
    note_sub = subparsers.add_parser("note", help="note element")
    note_sub.add_argument("--id")

    note_actions = note_sub.add_subparsers(dest="action", help="actions for working with notes ", required=True)

    # NOTE actions---
    note_add_sub = note_actions.add_parser("add", help="add new note")
    note_txt_sub = note_add_sub.add_argument('--text', required=True, nargs="*", help="type text of note, use str")
    note_category_sub = note_add_sub.add_argument('--category', required=True,
                                                  help="insert ID of note category, use int")

    note_list_sub = note_actions.add_parser("list")

    note_change_text_sub = note_actions.add_parser("change", help="change note text or category of the note")

    note_id_change_sub = note_change_text_sub.add_argument('--id', type=int, required=True,
                                                           help="insert ID changed note, use int")
    note_txt_change_sub = note_change_text_sub.add_argument('--text', nargs='*',
                                                            help="insert new text for note, use str")
    note_id_change_category_sub = note_change_text_sub.add_argument('--category', type=int,
                                                                    help="insert new ID of note category, use int")

    note_find_sub = note_actions.add_parser("find", help="find note by text, use str")
    note_id_find_sub = note_find_sub.add_argument('--text', required=True, nargs='*', help="insert text, use str")

    note_del_sub = note_actions.add_parser("delete", help="delete note")
    note_id_sub = note_del_sub.add_argument('--id', required=True, help="insert ID deleted note, use int")

    # CATEGORY parsers-------------------------------------------------------------------------------------------------

    category_sub = subparsers.add_parser("category", help="parser_category help")
    category_actions = category_sub.add_subparsers(dest="action", help="action help", required=True)

    # CATEGORY actions---
    category_add_sub = category_actions.add_parser("add")
    category_txt_sub = category_add_sub.add_argument('--text', nargs="*", required=True)

    category_list_sub = category_actions.add_parser("list")

    category_change_text_sub = category_actions.add_parser("change")
    category_id_change_sub = category_change_text_sub.add_argument('--id', type=int, required=True)
    category_txt_change_sub = category_change_text_sub.add_argument('--text', nargs="*", required=True)

    category_find_sub = category_actions.add_parser("find", help="find al notes with this category")
    category_id_find_sub = category_find_sub.add_argument('--id', required=True)

    category_clear_notes_sub = category_actions.add_parser("clear")
    category_id_clear_notes_sub = category_clear_notes_sub.add_argument('--id', required=True)

    category_del_sub = category_actions.add_parser("delete")
    category_id_sub = category_del_sub.add_argument('--id', required=True)

    args = parser.parse_args()
    return args
