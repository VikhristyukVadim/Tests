# import json
from flask import Flask, jsonify, request
from pony_file import db, insert_notes
from pony.orm import db_session

app = Flask(__name__)

client = app.test_client()

json_example = [
    {
        "id": 1,
        "quote": "The business plans of the next 10,000 years"
    },
    {
        "id": 2,
        "quote": "Last"
    }
]


@app.route("/example", methods=['GET'])
def get_list():
    print("==============", db.Notes)
    # return jsonify(json_example)

    result = {
        'data': []
    }
    with db_session:
        res = db.select(n for n in db.Notes)
        for i in res:
            result['data'].append({'quote': i.quote})
    return result, 200


@app.route("/example", methods=['POST'])
def update_list(message):
    # new_message = message
    insert_notes(message)
    # new_one = request.json
    # json_example.append(new_one)
    # return jsonify(json_example)
    return message, 200


@app.route("/example/<int:json_example_id>", methods=['PUT'])
def update_example(json_example_id):
    item = next((x for x in json_example if x['id'] == json_example_id), None)
    params = request.json
    if not item:
        return {'message': 'no examples with this id'}, 400
    item.update(params)
    return item


@app.route("/example/<int:json_example_id>", methods=['DELETE'])
def delete_example(json_example_id):
    idx, _ = next((x for x in enumerate(json_example) if x[1]['id'] == json_example_id), (None, None))
    json_example.pop(idx)
    return '', 204


if __name__ == "__main__":
    app.run()
# @app.route('/hello')
# def hello():
#     return '<div>Hello, World</div>'

# from markupsafe import escape
#
#
# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return f'User {escape(username)}'
#
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'
#
#
# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f'Subpath {escape(subpath)}'
