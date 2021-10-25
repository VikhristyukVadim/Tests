import requests
from pony import orm
from requests.exceptions import HTTPError, ConnectionError


def check_for_errors(fn):
    """
    function checking the presence of objects
    :param fn:
    :return:
    """
    def wrapper(*args):
        try:
            return fn(*args)
        except orm.core.ObjectNotFound:
            return {"status": "error", "message": "Record is not found"}, 404
        except Exception as err:
            return {"status": "error", "message": str(err)}, 500

    return wrapper


def result_to_json(note_id, message, category):

    """
    json generation for output in the table to the user
    :param note_id: id of the note
    :param message: text of the note
    :param category: category of the note
    :return: JSON
    """

    if note_id and message and category:
        return {"id": note_id, "quote": message, "category": category.category_name}
    elif category:
        return {"id": note_id, "quote": " ", "category": category}
    else:
        return {"id": note_id, "quote": message, "category": "----"}


def check_status(response):

    """
    check server response
    :param response:  server response
    :return: table with results
    """

    print('response-----------', response)
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    except ConnectionError as bad_connect:
        print(f'Problem with connect: {bad_connect}')
    else:
        table_width = 50
        res = response.json()
        if res.get('data') or res.get('category'):
            print('{:2} {:10} {:1}'.format('Id', 'Note'.center(table_width, '_'), "Category".center(10, ".")))
        if res.get('data'):
            for i in res['data']:
                print("{:2} {:.50} {:1}".format(i['id'], i['quote'].ljust(table_width, '.'), i['category'].center(10)))
        elif res.get('id'):
            print(
                "{:2} {:.50} {:1}".format(res['id'], res['quote'].ljust(table_width, ' '), res['category'].center(10)))
        elif res.get('message'):
            print(res['message'])
        elif res.get('category'):
            print("{:2} {:.60} {:40}".format(res['id'], " ".ljust(table_width, ' '), res['category'].center(10)))
        else:
            print(res)


def unite_txt(txt):
    return ' '.join(txt)


def create_args(res):

    """
    formation of the request body based on the received fields
    :param res:
    :return:
    """

    d = {}
    if hasattr(res, "id") and res.id is not None:
        d["id"] = res.id
    if hasattr(res, "text") and res.text is not None:
        d["quote"] = unite_txt(res.text)
    if hasattr(res, "category") and res.category is not None:
        d["category"] = unite_txt(res.category)
    if hasattr(res, "category_id") and res.category_id is not None:
        d["category_id"] = unite_txt(res.category_id)
    return d


def create_request(r):
    """
    formation of a request depending on the value in url
    :param r: str(action)
    :return: /..
    """
    if r == "add":
        return requests.post
    if r == "list" or r == "find":
        return requests.get
    if r == "change":
        return requests.put
    if r == "delete" or r == "clear":
        return requests.delete
