import json
from flask import jsonify

import server_app

"""new_note"""
"""search_note"""
"""del_note_by_id"""


def user_input():
    user_text = input("Input request: ")
    if user_text == "new_note":

        message = input("please input text: ")
        server_app.update_list(message)
        print("note_added vs name:", message)
    elif user_text == "search_note":
        input("Please input keyword: ")
        with open('db_example_file.JSON', 'r') as fh:
            jd1 = json.load(fh)
        print("search_note ", jd1)
    elif user_text == "list_note":
        note_list = server_app.get_list()
        # with open('db_example_file.JSON') as fh:
        #     jd1 = json.load(fh)
        print("note_list ", note_list)
    elif user_text == "del_note":
        note_id = input("insert ID:")
        print("note vs ID ", note_id, " is deleted")


user_input()

""" 1- набираем текст"""
""" 2- отсылаем на сервер """
""" 3- записывается в базу данных """
