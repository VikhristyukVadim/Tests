from flask import Flask, request
from pony_file import insert_notes, get_notes_list, del_note, find_by_word, change_by_id

app = Flask(__name__)

client = app.test_client()


@app.route('/list', methods=['GET'])
def get_list():
    result = get_notes_list()
    return result, 200


@app.route('/new_txt', methods=['POST'])
def add_item():
    content = request.json['data']
    n = insert_notes(content)
    return n, 200


@app.route("/change/<int:note_id>", methods=['PUT'])
def change_note_by_id(note_id):
    content = request.json['data']
    result = change_by_id(note_id, content)
    return result, 200


@app.route("/find/<note_text>", methods=['GET'])
def find_note_by_txt(note_text):
    data = find_by_word(note_text)
    return data, 200
    # if data is not None:
    #     return "You have find note num: " + data, 200
    # else:
    #     return "No matches found ", 205


@app.route("/delete/<int:note_id>", methods=['DELETE'])
def delete_note(note_id):
    del_note(note_id)
    return 'Object vs id ' + str(note_id) + ' is deleted', 200


if __name__ == "__main__":
    app.run()
