import requests


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


def look_for_errors(response, check_for_errors):
    if response.status_code != 200:
        raise check_for_errors(response.json()["message"])


def print_status(obj):
    print('status - ' + obj["status"], "---", obj["message"])
