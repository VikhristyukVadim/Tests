from flask import Flask, request
from pony import orm

from pony_file import insert_notes, get_notes_list, del_note, find_by_word, change_by_id

app = Flask(__name__)

client = app.test_client()


@app.route('/list', methods=['GET'])
def get_list():
    try:
        return get_notes_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route('/new_txt', methods=['POST'])
def add_item():
    content = request.json['data']
    print('request.json[]', content)
    try:
        return insert_notes(content)
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/change/<int:note_id>", methods=['PUT'])
def change_note_by_id(note_id):
    content = request.json['data']
    try:
        return change_by_id(note_id, content)
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/find/<note_text>", methods=['GET'])
def find_note_by_txt(note_text):
    try:
        return find_by_word(note_text)
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/delete/<int:note_id>", methods=['DELETE'])
def delete_note(note_id):
    try:
        return del_note(note_id)
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


if __name__ == "__main__":
    app.run()
