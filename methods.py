from pony import orm


def check_for_errors(fn):

    def wrapper(*args):
        try:
            return fn(*args)
        except orm.core.ObjectNotFound:
            return {"status": "error", "message": "Record is not found"}, 404
        except Exception as err:
            return {"status": "error", "message": str(err)}, 500

    return wrapper


def result_to_json(note_id, message):
    return {"id": note_id, "quote": message}
