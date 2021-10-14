from flask import Flask, request
from pony import orm

from pony_file import insert_notes, get_notes_list, del_note, find_by_word, change_by_id, create_category, del_category, \
    change_category, find_note_category, delete_all_category_notes, get_category_list, change_category_in_note

app = Flask(__name__)

client = app.test_client()


# Notes------------------------------------------------------------------------------------------------------------
# function for creating new note, need id of category
@app.route('/add_note', methods=['POST'])
def add_new_note():
    req = request.json
    try:
        return insert_notes(req['quote'], req['category'])
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to query the list of note
@app.route('/list_notes', methods=['GET'])
def get_list():
    try:
        return get_notes_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to search note by word
@app.route("/find_note", methods=['GET'])
def find_note_by_txt():
    req = request.json
    try:
        return find_by_word(req["quote"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to change note category
@app.route("/change_note", methods=['PUT'])
def change_note_category():
    req = request.json
    print('req', req)
    try:
        return change_by_id(req["id"], req['quote'])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function for replacing the text of note
@app.route("/change_category", methods=['PUT'])
def change_note_by_id():
    res = request.json
    print('req', res)
    try:
        return change_category_in_note(res["id"], res["category_id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to delete note
@app.route("/delete_note", methods=['DELETE'])
def delete_note():
    req = request.json
    try:
        return del_note(req['id'])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# Category -------------------------------------------------------------------------------------------------

# function for creating new category of notes
@app.route("/add_category", methods=['POST'])
def add_category():
    req = request.json
    try:
        return create_category(req["quote"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to query the list of note
@app.route('/list_category', methods=['GET'])
def get_cat_list():
    try:
        return get_category_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to change the name of the category of the note
@app.route("/change_name", methods=['PUT'])
def change_category_by_id():
    req = request.json
    try:
        return change_category(req["id"], req["quote"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to delete all notes in a category
@app.route("/clear", methods=['DELETE'])
def delete_all_in_category():
    req = request.json
    try:
        return delete_all_category_notes(req["id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function to search the category of notes
@app.route("/find_category_note", methods=['GET'])
def find_note_by_category():
    req = request.json
    try:
        return find_note_category(req["id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


# function for replacing the category of notes
@app.route("/delete_category", methods=['DELETE'])
def del_category_by_id():
    req = request.json
    try:
        return del_category(req["id"])
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


if __name__ == "__main__":
    app.run()
