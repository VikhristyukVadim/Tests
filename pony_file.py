from pony.orm import *

from methods import result_to_json

db = Database('sqlite', 'my_db.sqlite', create_db=True)


# Create data base entity_____________________________________________________________________________________________
class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    category_name = Required(str, unique=True)
    items = Set(lambda: Notes, reverse='category')


class Notes(db.Entity):
    id = PrimaryKey(int, auto=True)
    quote = Required(str)
    category = Optional(Category, reverse='items')


# NOTES_METHODS_______________________________________________________________________________________________________
@db_session
def insert_notes(note_txt, note_category):
    if Category[note_category]:
        new_note = Notes(quote=note_txt, category=note_category)
        commit()
        return result_to_json(new_note.id, new_note.quote, new_note.category)
    else:
        return {"status": "error", "message": "Category is not found"}, 404


@db_session
def get_notes_list():
    n = Notes.select()
    result = {'data': []}
    for i in n:
        result['data'].append(result_to_json(i.id, i.quote, i.category))
    return result


@db_session
def find_by_word(search_text):
    product_list = Notes.select(lambda note: search_text in note.quote).limit(10)
    notes = []
    if product_list:
        for i in product_list:
            notes.append({'id': i.id, 'quote': i.quote, "category": i.category.category_name})
        return {"data": notes}
    else:
        return {"status": "error", "message": "Record is not found"}, 404


@db_session
def change_by_id(note_id, new_txt):
    data = Notes[note_id]
    data.quote = new_txt
    return result_to_json(data.id, data.quote, data.category)


@db_session
def del_note(note_id):
    Notes[note_id].delete()
    return {"status": "ok", "message": "record is deleted"}


@db_session
def change_category_in_note(note_id, category_id):
    note = Notes.get(id=note_id)
    category = Category[category_id]
    note.category = category.id
    commit()
    return {"status": "ok", "message": "Record category is changed"}


# CATEGORY_METHODS____________________________________________________________________________________________________
@db_session
def create_category(new_name):
    new_category = Category(category_name=new_name)
    commit()
    return result_to_json(new_category.id, None, new_category.category_name)


@db_session
def get_category_list():
    category_list = Category.select()
    result = {'data': []}
    for i in category_list:
        result['data'].append(result_to_json(i.id, None, i.category_name))
    return result


@db_session
def del_category(category_id):
    Category[category_id].delete()
    return {"status": "ok", "message": "record is deleted"}


@db_session
def change_category(category_id, category_new_txt):
    data = Category[category_id]
    data.category_name = category_new_txt
    return result_to_json(data.id, None, data.category_name)


@db_session
def find_note_category(note_category_id):
    product_list = Notes.select(lambda note: note.category.id == note_category_id).limit(10)
    notes = []
    if product_list:
        for i in product_list:
            notes.append({'id': i.id, 'quote': i.quote, 'category': i.category.category_name})
        return {"data": notes}
    else:
        return {"status": "error", "message": "Record is not found"}, 404


@db_session
def delete_all_category_notes(note_category_id):
    Notes.select(lambda note: note.category.id == note_category_id).delete()
    commit()
    return {"status": "ok", "message": "All record is deleted"}


db.generate_mapping(create_tables=True)
