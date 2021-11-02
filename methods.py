import requests
from pony import orm
from requests.exceptions import HTTPError, ConnectionError


def check_for_errors(response):
    """
    function checking the presence of objects
    :param response:
    :return:
    """

    try:
        response.raise_for_status()
    except orm.core.ObjectNotFound:
        return {"status": "error", "message": "Record is not found"}, 404
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    except ConnectionError as bad_connect:
        print(f'Problem with connect: {bad_connect}')
    else:
        return response


def result_to_json(note_id, record, category):
    """
    json generation for output in the table to the user
    :param note_id: id of the note
    :param record: text of the note
    :param category: category of the note
    :return: JSON
    """
    if note_id and record and category is not None:
        return {"id": note_id, "record": record, "category": {"id": category["id"], "name": category["name"]}}
    elif note_id and record and category is None:
        return {"id": note_id, "record": record, "category": None}
    elif category:
        return {"id": note_id, "name": category}
    else:
        return {"id": note_id, "record": record, "name": "----"}


def unite_txt(txt):
    if txt is not None:
        return ' '.join(txt)
    else:
        return None


def create_request(r):
    """
    formation of a request depending on the value in url
    :param r: str(action)
    :return: /..
    """
    if r == "add":
        return requests.post
    if r == "list" or r == "find" or r == "find-note":
        return requests.get
    if r == "change":
        return requests.put
    if r == "delete" or r == "clear":
        return requests.delete


def check_status(obj):
    if isinstance(obj, type):
        return
    elif not obj:
        print("--> There are no objects")
    elif obj and "message" in obj:
        print('status - ' + obj["status"], "---", obj["message"])
    else:
        return obj
