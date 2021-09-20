from pony.orm import *

db = Database('sqlite', 'my_db.sqlite', create_db=True)


@db_session
class Notes(db.Entity):
    quote = Required(str)


def insert_notes(message):
    print("=============", message)
    Notes(quote=message)


def get_notes_list(message):
    print("=============", message)
    Notes(quote=message)


# set_sql_debug(True)
db.generate_mapping(create_tables=True)
