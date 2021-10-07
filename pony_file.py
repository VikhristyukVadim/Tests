from pony.orm import *

from methods import result_to_json

db = Database('sqlite', 'my_db.sqlite', create_db=True)

# ----------------------------------
"""Create data base entity"""


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    category_name = Required(str, unique=True)
    items = Set(lambda: Notes, reverse='category')


class Notes(db.Entity):
    id = PrimaryKey(int, auto=True)
    quote = Required(str)
    category = Optional(Category, reverse='items')


# ----------------------------------

@db_session
def insert_notes(message, c_id):
    if Category[int(c_id)]:
        n = Notes(quote=message, category=int(c_id))
        commit()
        return result_to_json(n.id, n.quote, n.category)
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
def find_by_word(new_txt):
    product_list = Notes.select(lambda note: new_txt in note.quote).limit(10)
    notes = []
    if product_list:
        for i in product_list:
            notes.append({'id': i.id, 'quote': i.quote})
        return {"data": notes}
    else:
        return {"status": "error", "message": "Record is not found"}, 404


@db_session
def change_by_id(item_id, new_txt):
    data = Notes[item_id]
    data.quote = new_txt
    return result_to_json(data.id, data.quote, data.category)


@db_session
def del_note(del_id):
    Notes[del_id].delete()
    return {"status": "ok", "message": "record is deleted"}


# -----------------------------------------------------------------

"""CATEGORY"""


# ------------------------------------------------------------------


@db_session
def create_category(txt):
    c = Category(category_name=txt)
    commit()
    return result_to_json(c.id, None, c.category_name)


@db_session
def get_category_list():
    c = Category.select()
    result = {'data': []}
    for i in c:
        result['data'].append(result_to_json(i.id, None, i.category_name))
    return result


@db_session
def del_cat(del_id):
    c = Category[del_id]
    print('c',c)
    Category[del_id].delete()
    return {"status": "ok", "message": "record is deleted"}


@db_session
def change_c_by_id(item_id, new_txt):
    data = Category[item_id]
    data.category_name = new_txt
    return result_to_json(data.id, None, data.category_name)


@db_session
def find_n_in_cat(c_id):
    product_list = Notes.select(lambda note: note.category.id == c_id).limit(10)
    notes = []
    if product_list:
        for i in product_list:
            notes.append({'id': i.id, 'quote': i.quote, 'category': i.category.category_name})
        return {"data": notes}
    else:
        return {"status": "error", "message": "Record is not found"}, 404


@db_session
def del_all_note(c_id):
    del_list = Notes.select(lambda note: note.category.id == c_id).limit()
    for i in del_list:
        Notes[i.id].delete()
    return {"status": "ok", "message": "All record is deleted"}


@db_session
def ch_n_cat(n_id, c_id):
    n = Notes.get(id=n_id)
    c = Category[c_id]
    n.category = c.id
    commit()
    return {"status": "ok", "message": "Record category is changed"}


db.generate_mapping(create_tables=True)
