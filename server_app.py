from flask import Flask
from pony_file import insert_notes, get_notes_list, change_note, del_note

app = Flask(__name__)

client = app.test_client()


@app.route("/example", methods=['GET'])
def get_list():
    result = get_notes_list()
    print('NOTES_LIST: ', result['data'])
    return result, 200


@app.route("/example", methods=['POST'])
def add_item(message):
    insert_notes(message)
    print('Your new note is added successfully: ', message)
    return message, 200


@app.route("/example", methods=['PUT'])
def change_note_by_id(new_txt):
    data = change_note(new_txt)
    print('You have changed the note.')
    return data, 200


@app.route("/example", methods=['PUT'])
def find_note_by_txt(word):
    data = change_note(word)
    print('You have find note num', data)
    return data, 200


@app.route("/example", methods=['DELETE'])
def delete_note(note_id):
    del_note(note_id)
    return 'Object vs id = {note_id} deleted', 204


if __name__ == "__main__":
    app.run()
