from pony import orm
from requests.exceptions import HTTPError, ConnectionError


def check_for_errors(fn):
    def wrapper(*args):
        try:
            return fn(*args)
        except orm.core.ObjectNotFound:
            return {"status": "error", "message": "Record is not found"}, 404
        except Exception as err:
            return {"status": "error", "message": str(err)}, 500
    return wrapper


def result_to_json(note_id, message, category):
    print('note_id, message, category', note_id, message, category)
    if note_id and message and category:
        return {"id": note_id, "quote": message, "category": category.category_name}
    elif category:
        print('category', category)
        return {"id": note_id, "quote": " ", "category": category}
    else:
        return {"id": note_id, "quote": message, "category": "----"}


def check_status(response):
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
        # print('res============', res)
        if res.get('data') or res.get('category'):
            print('{:1} {:10} {:1}'.format('Id', 'Note'.center(table_width, '_'), "Category".center(10, ".")))
        if res.get('data'):
            for i in res['data']:
                print("{:1} {:.50} {:1}".format(i['id'], i['quote'].ljust(table_width, ' '), i['category'].center(10)))
        elif res.get('id'):
            print(
                "{:1} {:.50} {:1}".format(res['id'], res['quote'].ljust(table_width, ' '), res['category'].center(10)))
        elif res.get('message'):
            print(res['message'])
        elif res.get('category'):
            print('res',res)
            print("{:1} {:.60} {:40}".format(res['id'], " ".ljust(table_width, ' '), res['category'].center(10)))
        else:
            print(res)
