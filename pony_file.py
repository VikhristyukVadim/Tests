from pony.orm import *

from methods import result_to_json

db = Database('sqlite', 'my_db.sqlite', create_db=True)


# Create data base entity_____________________________________________________________________________________________
class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    items = Set(lambda: Notes, reverse='category')


class Notes(db.Entity):
    id = PrimaryKey(int, auto=True)
    record = Required(str)
    category = Optional(Category, reverse='items')


# NOTES_METHODS_______________________________________________________________________________________________________
@db_session
def insert_notes(note_txt, note_category):
    """
    adding a new note

    :param note_txt: type(str)- record
    :param note_category: type(int)- category id
    :return: type(dict)- added note (id,record,category)
    """
    if Category[note_category]:
        new_note = Notes(record=note_txt, category=note_category)
        commit()
        return result_to_json(new_note.id, new_note.record,
                              category={"id": new_note.category.id, "name": new_note.category.name})
    else:
        return {"status": "error", "message": "Category is not found"}, 404


@db_session
def get_notes_list():
    """
    getting a list of notes

    :return: type(dict)- list of te notes (id, record)
    """
    n = Notes.select()
    result = {'data': []}
    for i in n:
        result['data'].append(result_to_json(i.id, i.record,
                                             category={"id": i.category.id,
                                                       "name": i.category.name} if i.category is not None else None))
    return result


@db_session
def change_note_by_id(note_id, new_txt):
    """
    change the text of the note

    :param note_id: type(int)- id
    :param new_txt: type(str)- record
    :return: type(dict)- changed note (id,record,name)
    """
    data = Notes[note_id]
    data.record = new_txt
    return {"status": "ok", "message": "Record is changed"}
    # return result_to_json(data.id, data.record, category={"id": data.category.id, "name": data.category.name})


@db_session
def change_category_in_note(note_id, category_id):
    """
    change note category

    :param note_id: type(int)- id
    :param category_id: type(int)- id
    :return: ok
    """
    note = Notes.get(id=note_id)
    category = Category[category_id]
    note.category = category.id
    commit()
    return {"status": "ok", "message": "Record category is changed"}


@db_session
def find_by_word(search_text):
    """
    search notes by word

    :param search_text: type(str)- text
    :return: type(dict)- list of notes(id,record,category)
    """
    product_list = Notes.select(lambda note: search_text in note.record).limit(10)
    result = {'data': []}
    if product_list:
        for i in product_list:
            result['data'].append(
                result_to_json(i.id, i.record, category={"id": i.category.id,
                                                         "name": i.category.name} if i.category is not None else None))
        return result
    else:
        return {"status": "error", "message": "Record is not found"}, 404


@db_session
def del_note(note_id):
    """
    deleting note

    :param note_id: type(int)- id
    :return: ok
    """
    Notes[note_id].delete()
    return {"status": "ok", "message": "Note with ID:" + note_id + " - was deleted"}


# CATEGORY_METHODS____________________________________________________________________________________________________
@db_session
def create_category(new_name):
    """
    create a new category of notes

    :param new_name: type(str)- new name of category
    :return: type(dict)- added category(id,name)
    """
    new_category = Category(name=new_name)
    commit()
    return result_to_json(new_category.id, None, new_category.name)


@db_session
def get_category_list():
    """
    a list of category

    :return: type(dict)- list of category (id,name)
    """
    category_list = Category.select()
    result = {'data': []}
    for i in category_list:
        result['data'].append(result_to_json(i.id, None, i.name))
    return result


@db_session
def change_category(category_id, category_new_txt):
    """
    change the name of the category of a note

    :param category_id: type(int)- id
    :param category_new_txt: type(str)- name
    :return: type(dict)- new name(id,name)
    """
    data = Category[category_id]
    data.name = category_new_txt
    return result_to_json(data.id, None, data.name)


@db_session
def find_note_category(note_category_id):
    """
    return all notes in a category

    :param note_category_id: type(int)- id
    :return: type(dict)- the list of notes (id,record,name)
    """
    product_list = Notes.select(lambda note: note.category.id == note_category_id).limit(10)
    result = {'data': []}
    if product_list:
        for i in product_list:
            result["data"].append(
                {'id': i.id, 'record': i.record, 'category': {"id": i.category.id, "name": i.category.name}})
        return result
    else:
        return {"status": "error", "message": "Record is not found"}, 404


@db_session
def delete_all_category_notes(note_category_id):
    """
    that deletes all notes in a category

    :param note_category_id: type(int)- id
    :return: ok
    """
    Category[note_category_id].items.select().delete()
    Notes.select(lambda note: note.category.id == note_category_id).delete()
    commit()
    return {"status": "ok", "message": "All records from this Category was deleted"}


@db_session
def del_category(category_id):
    """
    delete selected category

    :param category_id: type(int)- id
    :return: ok
    """
    Category[category_id].delete()
    return {"status": "ok", "message": "Category with ID:" + category_id + " - was deleted"}


db.generate_mapping(create_tables=True)
