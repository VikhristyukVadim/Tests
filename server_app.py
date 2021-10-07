from flask import Flask, request
from pony import orm

from pony_file import insert_notes, get_notes_list, del_note, find_by_word, change_by_id, create_category, del_cat, \
    change_c_by_id, find_n_in_cat, del_all_note, get_category_list, ch_n_cat

app = Flask(__name__)

client = app.test_client()


@app.route('/list', methods=['GET'])
def get_list():
    try:
        return get_notes_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route('/new_txt/<c_id>', methods=['POST'])
def add_item(c_id):
    content = request.json['data']
    try:
        return insert_notes(content, c_id)
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


# -------------------------------------------------------------------------------------------------

@app.route("/c_add", methods=['POST'])
def add_category():
    content = request.json['data']
    try:
        return create_category(content)
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route('/c_list', methods=['GET'])
def get_cat_list():
    try:
        return get_category_list()
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/c_del/<int:c_id>", methods=['DELETE'])
def del_category(c_id):
    try:
        return del_cat(c_id)
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/c_edit/<int:c_id>", methods=['PUT'])
def change_category_by_id(c_id):
    content = request.json['data']
    try:
        return change_c_by_id(c_id, content)
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/find_n/<int:c_id>", methods=['GET'])
def find_note_by_category(c_id):
    try:
        return find_n_in_cat(int(c_id))
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/del_n_in_cat/<int:c_id>", methods=['DELETE'])
def delete_all_in_cat(c_id):
    print('category',c_id)
    try:
        c = del_all_note(int(c_id))
        return c
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


@app.route("/ch_n_cat", methods=['PUT'])
def ch_note_category():
    req = request.json['data']
    try:
        return ch_n_cat(int(req[0]), int(req[1]))
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except Exception as err:
        return {"status": "error", "message": str(err)}, 500


if __name__ == "__main__":
    app.run()
