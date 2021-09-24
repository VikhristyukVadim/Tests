from pony.orm import *

db = Database('sqlite', 'my_db.sqlite', create_db=True)


class Notes(db.Entity):
    quote = Required(str)


@db_session
def insert_notes(message):
    Notes(quote=message)
    return Notes.select().count()


@db_session
def get_notes_list():
    result = {
        'data': []
    }
    res = Notes.select()
    for i in res:
        result['data'].append({"id = " + str(i.id): i.quote})
    return result


@db_session
def change_by_word(new_txt):
    data = Notes.select()
    for i in data:
        res = i.quote.split().count(new_txt)
        if res > 0:
            result = str(i.id) + ":  " + i.quote
            return result


@db_session
def change_by_id(item_id, new_txt):
    data = Notes.select()
    for i in data:
        if item_id == i.id:
            i.quote = new_txt
            return 'You have changed note with id:  ' + str(i.id) + '  to the text:  ' + str(i.quote)


@db_session
def del_note(del_id):
    deleted_element = Notes.get(id=del_id)
    deleted_element.delete()


db.generate_mapping(create_tables=True)
