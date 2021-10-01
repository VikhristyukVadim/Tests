from pony import orm

answer = {'data': [
    {
        "status": "ok",
        "message": "note deleted successfully"},
    {
        "status": "error",
        "message": "note not found"}
]}


def check_for_errors(fn):
    def wrapper(*args):
        try:
            fn(*args)
            if fn(*args)['data']:
                print('fn(*args)', fn(*args))
                return fn(*args)
            else:
                return answer['data'][0]
        except orm.core.ObjectNotFound:
            return answer['data'][1]

    return wrapper


def result_to_json(note_id, message):
    return {'id': note_id, "quote": message}
