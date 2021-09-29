from pony.orm import *

db = Database('sqlite', 'my_db.sqlite', create_db=True)

set_sql_debug(True)


def result_to_json(note_id, message):
    return {'data': [{'id': note_id}, {"quote": message}]}


class Notes(db.Entity):
    note_id = PrimaryKey(int)
    quote = Required(str)


@db_session
def insert_notes(message):
    notes_select = Notes.select()
    j = 0
    for i in notes_select:
        if i.note_id > j:
            j = i.note_id
    Notes(quote=message, note_id=j + 1)
    return result_to_json(j, message)


@db_session
def get_notes_list():
    result = {'data': []}
    res = Notes.select()
    for i in res:
        result['data'].append({str(i.note_id): i.quote})
    return result


@db_session
def find_by_word(new_txt):
    product_list = Notes.select(lambda note: note.quote == new_txt)[:]
    # ae = db.get("select quote from Notes where quote = $new_txt")
    # print('ae============================',ae)
    notes = []
    for i in product_list:
        notes.extend([{'id': i.note_id}, {'quote': i.quote}])
    return {"data": notes}


@db_session
def change_by_id(item_id, new_txt):
    data = Notes.select()
    for i in data:
        if item_id == i.note_id:
            i.quote = new_txt
            return result_to_json(i.note_id, i.quote)


@db_session
def del_note(del_id):
    deleted_element = Notes.get(id=del_id)
    deleted_element.delete()
    return del_id


db.generate_mapping(create_tables=True)
