from flask import Flask, request
from pony import orm

from pony_file import insert_notes, get_notes_list, del_note, find_by_word, change_note_by_id, create_category, \
    del_category, change_category, find_note_category, delete_all_category_notes, get_category_list, \
    change_category_in_note

app = Flask(__name__)

client = app.test_client()


# Notes------------------------------------------------------------------------------------------------------------
@app.route('/note/add', methods=['POST'])
def add_new_note():

    """
    for creating new note, need id of category
    :return: type(dict)- added note (id,quote,category)
    """
    req = request.json

    try:
        return insert_notes(req['quote'], req['category'])
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route('/note/list', methods=['GET'])
def get_list():
    """
    requesting a list of notes
    :return: type(dict)- list of te notes (id, quotes)
    """
    try:
        return get_notes_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/note/change", methods=['PUT'])
def change_note():
    """
    to change note
    :return: type(dict)- changed note (id,quote,category_name)
    """
    res = request.json
    try:
        if "category_id" in res and res["category_id"] is not None:
            return change_category_in_note(res["id"], res["category_id"])
        elif "quote" in res and res["quote"] is not None:
            return change_note_by_id(res["id"], res['quote'])

    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/note/find", methods=['GET'])
def find_note_by_txt():
    """
    to find note by word

    :return: type(dict)- found notes (id,quote,category_name)
    """
    req = request.json
    try:
        return find_by_word(req["quote"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/note/delete", methods=['DELETE'])
def delete_note():
    """
    for deleting note
    :return: status": "ok"
    """
    req = request.json
    try:
        return del_note(req['id'])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# Category -------------------------------------------------------------------------------------------------

@app.route("/category/add", methods=['POST'])
def add_category():
    """
    for create a new category of notes
    :return: type(dict)- new category (id,category_name)
    """
    req = request.json
    try:
        return create_category(req["quote"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route('/category/list', methods=['GET'])
def get_cat_list():
    """
    requesting a list of category
    :return: type(dict)- list of category (id,category_name)
    """
    try:
        return get_category_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/category/change", methods=['PUT'])
def change_category_by_id():
    """
    changing the name of the category of a note
    :return: type(dict)- new category_name(id,category_name)
    """
    req = request.json

    try:
        return change_category(req["id"], req["quote"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/category/clear", methods=['DELETE'])
def delete_all_in_category():
    """
    that deletes all notes in a category
    :return:"status": "ok"
    """
    req = request.json
    try:
        return delete_all_category_notes(req["id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/category/find-note", methods=['GET'])
def find_note_by_category():
    """
    displaying all notes in a category
    :return: type(dict)- the list of notes (id,quote,category_name)
    """
    req = request.json
    try:
        return find_note_category(req["id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/category/delete", methods=['DELETE'])
def del_category_by_id():
    """
    to change the category of the note
    :return: "status": "ok"
    """
    req = request.json
    try:
        return del_category(req["id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


if __name__ == "__main__":
    app.run()
