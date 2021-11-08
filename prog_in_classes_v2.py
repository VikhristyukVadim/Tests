from argparse_methods import argument_parser
from methods import create_request, unite_txt, look_for_errors, print_status


class Note:
    def __init__(self, id=None, record=None, category=None):
        self.id = id
        self.record = record

        self.category = category

    @staticmethod
    def request_name():
        return "note"

    @staticmethod
    def show_table_headers():
        print(
            "{:} {:2} {:.50} {:} {:.10} {:2} {:}".format(
                "|", "ID", "Note_name".center(50, "_"), "|", "Category".center(10, "_"), "ID", "|"))

    @staticmethod
    def from_json(resp):
        return Note(resp["id"], resp["record"], resp["category"])

    def to_json(self):
        return {
            "id": self.id,
            "record": self.record,
            "category": self.category
        }

    def print_item(self):
        print("id:   {}".format(self.id))
        print("record: {}".format(self.record))
        print("category: {}".format(self.category))

    def print_table(self):
        print("{:} {:2} {:.50} {:} {:.10} {:2} {:}".format(
            "|", self.id, self.record.center(50, "."), "|",
            self.category["name"].center(10, "."), self.category["id"], "|"))


class Category:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @staticmethod
    def request_name():
        return "category"

    @staticmethod
    def from_json(resp):
        return Category(resp["id"], resp['name'])

    @staticmethod
    def show_table_headers():
        print(
            "{:} {:2} {:.50} {:1}".format("|", "ID", "Category_name".center(50, "_"), "|"))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def print_item(self):
        print("id:   {}".format(self.id))
        print("name: {}".format(self.name))

    def print_table(self):
        print("{:} {:2} {:.50} {:1}".format("|", self.id, self.name.center(50, "."), "|"))


class CheckForErrors(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        if self.message:
            return 'ERROR, {0} '.format(self.message)
        else:
            return 'ERROR has been raised'


class Server:
    def __init__(self, address):
        self.address = address

    def _send_request(self, name, api, data=None):
        ready_request = create_request(api)
        return ready_request(self.address + "/" + name + "/" + api, json=data)

    def add(self, item):
        resp = self._send_request(item.request_name(), "add", item.to_json())

        look_for_errors(resp, CheckForErrors)

        return item.from_json(resp.json())

    def list(self, item):
        resp = self._send_request(item.request_name(), "list")

        look_for_errors(resp, CheckForErrors)

        if resp is not None:
            item_list = []
            for i in resp.json()["data"]:
                if "category" and "record" in i:
                    item_list.append(Note.from_json(i))
                else:
                    item_list.append(Category.from_json(i))
            return item_list

    def change(self, item):
        resp = self._send_request(item.request_name(), "change", item.to_json())

        look_for_errors(resp, CheckForErrors)

        return resp.json()

    def find(self, item_value, item):
        if item.request_name() == "note":
            resp = self._send_request(item.request_name(), "find", item_value)

            look_for_errors(resp, CheckForErrors)

            if resp is not None:
                item_list = []
                for i in resp.json()["data"]:
                    item_list.append(Note.from_json(i))
                return item_list
        elif item.request_name() == "category":
            resp = self._send_request(item.request_name(), "find-note", item_value)

            look_for_errors(resp, CheckForErrors)

            if resp is not None:
                item_list = []
                for i in resp.json()["data"]:
                    item_list.append(Note.from_json(i))
                return item_list

    def delete(self, item_id, item):
        resp = self._send_request(item.request_name(), "delete", item_id)

        look_for_errors(resp, CheckForErrors)

        return resp.json() if hasattr(resp, "json") else resp

    def clear(self, item_id, item):
        resp = self._send_request(item.request_name(), "clear", item_id)

        look_for_errors(resp, CheckForErrors)

        return resp.json() if hasattr(resp, "json") else resp


if __name__ == '__main__':

    def result(args_values):
        """
        Processing requests
        :param args_values:
        :return:
        """
        try:
            # NOTES_____________________________________________________________________________________________________
            if args_values.object == "note":
                if args_values.action == "add":
                    obj = Server(args_values.server).add(Note(0, unite_txt(args_values.text), args_values.category))
                    obj.print_item()

                elif args_values.action == "list":
                    obj = Server(args_values.server).list(Note)
                    Note.show_table_headers()
                    for i in obj:
                        i.print_table()

                elif args_values.action == "change":
                    if args_values.text is None and args_values.category is None:
                        print("please enter --category(id) or --text of the Notes(str)")
                    else:
                        obj = Server(args_values.server).change(
                            Note(args_values.id, unite_txt(args_values.text), args_values.category))
                        print_status(obj)

                elif args_values.action == "find":
                    obj = Server(args_values.server).find(unite_txt(args_values.text), Note)
                    Note.show_table_headers()
                    for i in obj:
                        i.print_table()

                elif args_values.action == "delete":
                    obj = Server(args_values.server).delete(args_values.id, Note)
                    print_status(obj)

            # CATEGORY_____________________________________________________________________________________________________________
            elif args_values.object == "category":
                if args_values.action == "add":
                    obj = Server(args_values.server).add(Category(0, unite_txt(args_values.text)))
                    obj.print_item()

                elif args_values.action == "list":
                    obj = Server(args_values.server).list(Category)
                    Category.show_table_headers()
                    for i in obj:
                        i.print_table()

                elif args_values.action == "change":
                    obj = Server(args_values.server).change(Category(args_values.id, unite_txt(args_values.text)))
                    obj.print_item()

                elif args_values.action == "find":
                    obj = Server(args_values.server).find(args_values.id, Category)
                    Note.show_table_headers()
                    for i in obj:
                        i.print_table()

                elif args_values.action == "clear":
                    obj = Server(args_values.server).clear(args_values.id, Category)
                    print_status(obj)

                elif args_values.action == "delete":
                    obj = Server(args_values.server).delete(args_values.id, Category)
                    print_status(obj)

        except CheckForErrors as err:
            print(f'Error occurred: {err}')


    result(argument_parser())
