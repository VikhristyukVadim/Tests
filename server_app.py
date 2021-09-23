from flask import Flask, request, jsonify
from pony_file import insert_notes, get_notes_list, del_note, change_by_word, change_by_id

app = Flask(__name__)

client = app.test_client()


@app.route('/example/list', methods=['GET'])
def get_list():
    result = get_notes_list()
    # print('NOTES_LIST: ', result['data'])
    return result, 200


@app.route('/example/new_txt', methods=['POST'])
def add_item():
    content = request.form['data']
    insert_notes(content)
    return content, 200
    # insert_notes(new_txt)
    # print('Your new note is added successfully: ', new_txt)
    # return new_txt, 200


@app.route("/example", methods=['PUT'])
def change_note_by_id(new_txt):
    data = change_by_id(new_txt)
    print('You have changed the note.')
    return data, 200


@app.route("/example", methods=['PUT'])
def find_note_by_txt(word):
    data = change_by_word(word)
    print('You have find note num', data)
    return data, 200


@app.route("/example", methods=['DELETE'])
def delete_note(note_id):
    del_note(note_id)
    return 'Object vs id = {note_id} deleted', 204


if __name__ == "__main__":
    app.run()
