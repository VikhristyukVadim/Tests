from pony.orm import *

from Tests.methods import check_for_errors, result_to_json

db = Database('sqlite', 'my_db.sqlite', create_db=True)

# ----------------------------------
"""Create data base entity"""


class Notes(db.Entity):
    id = PrimaryKey(int, auto=True)
    quote = Required(str)


# ----------------------------------

@db_session
def insert_notes(message):
    n = Notes(quote=message)
    commit()
    return {'data': [result_to_json(n.id, n.quote)]}


@db_session
def get_notes_list():
    n = Notes.select()
    result = {'data': []}
    for i in n:
        result['data'].append(result_to_json(i.id, i.quote))
    return result


@check_for_errors
@db_session
def find_by_word(new_txt):
    product_list = Notes.select(lambda note: new_txt in note.quote).limit(10)
    notes = []
    for i in product_list:
        notes.append({'id': i.id, 'quote': i.quote})
    return {"data": notes}


@check_for_errors
@db_session
def change_by_id(item_id, new_txt):
    data = Notes[item_id]
    data.quote = new_txt
    return {'data': [result_to_json(data.id, data.quote)]}


@check_for_errors
@db_session
def del_note(del_id):
    Notes[del_id].delete()


db.generate_mapping(create_tables=True)
