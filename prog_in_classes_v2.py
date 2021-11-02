from argparse_methods import argument_parser
from methods import create_request, unite_txt, check_for_errors, check_status

"""Default server"""

server_way = 'http://127.0.0.1:5000'


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
        print("def from_json(resp)::::", resp)
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


class Server:
    def __init__(self, address):
        self.address = address

    def _send_request(self, name, api, data=None):
        ready_request = create_request(api)
        return ready_request(self.address + "/" + name + "/" + api, json=data)

    def add(self, item):
        resp = check_for_errors(self._send_request(item.request_name(), "add", item.to_json()))
        if resp is not None:
            return item.from_json(resp.json())

    def list(self, item):
        resp = check_for_errors(self._send_request(item.request_name(), "list"))
        if resp is not None:
            item_list = []
            for i in resp.json()["data"]:
                if "category" and "record" in i:
                    item_list.append(Note.from_json(i))
                else:
                    item_list.append(Category.from_json(i))
            return item_list

    def change(self, item):
        resp = check_for_errors(self._send_request(item.request_name(), "change", item.to_json()))
        if resp is not None:
            if "id" in resp.json():
                return item.from_json(resp.json())
            else:
                return resp.json()

    def find(self, item_value, item):
        if item.request_name() == "note":
            resp = check_for_errors(self._send_request(item.request_name(), "find", item_value))
            if resp is not None:
                item_list = []
                for i in resp.json()["data"]:
                    item_list.append(Note.from_json(i))
                return item_list
        elif item.request_name() == "category":
            resp = check_for_errors(self._send_request(item.request_name(), "find-note", item_value))
            if resp is not None:
                item_list = []
                for i in resp.json()["data"]:
                    item_list.append(Note.from_json(i))
                return item_list

    def delete(self, item_id, item):
        resp = check_for_errors(self._send_request(item.request_name(), "delete", item_id))
        return resp.json() if hasattr(resp, "json") else resp

    def clear(self, item_id, item):
        resp = check_for_errors(self._send_request(item.request_name(), "clear", item_id))
        return resp.json() if hasattr(resp, "json") else resp


if __name__ == '__main__':

    # NOTES_____________________________________________________________________________________________________________
    def result(args_values):
        """
        Processing requests
        :param args_values:
        :return:
        """
        if args_values.object == "note":
            if args_values.action == "add":
                obj = Server(server_way).add(Note(0, unite_txt(args_values.text), args_values.category))
                if obj is not None:
                    check_status(obj.to_json())
                    obj.print_item()

            elif args_values.action == "list":
                obj = Server(server_way).list(Note)
                if obj is not None:
                    check_status(obj)
                    Note.show_table_headers()
                    for i in obj:
                        i.print_table()

            elif args_values.action == "change":
                if args_values.text is not None or args_values.category is not None:
                    obj = Server(server_way).change(
                        Note(args_values.id, unite_txt(args_values.text), args_values.category))
                    if obj is not None:
                        check_status(obj)

            elif args_values.action == "find":
                obj = Server(server_way).find(unite_txt(args_values.text), Note)
                check_status(obj)
                if obj is not None:
                    Note.show_table_headers()
                    for i in obj:
                        i.print_table()

            elif args_values.action == "delete":
                obj = Server(server_way).delete(args_values.id, Note)
                check_status(obj)

        # CATEGORY_____________________________________________________________________________________________________________
        elif args_values.object == "category":
            if args_values.action == "add":
                obj = Server(server_way).add(Category(0, unite_txt(args_values.text)))
                if obj is not None:
                    check_status(obj.to_json())
                    obj.print_item()

            elif args_values.action == "list":
                obj = Server(server_way).list(Category)
                if obj is not None:
                    check_status(obj)
                    if len(obj) != 0:
                        Category.show_table_headers()
                        for i in obj:
                            i.print_table()

            elif args_values.action == "change":
                obj = Server(server_way).change(Category(args_values.id, unite_txt(args_values.text)))
                if obj is not None:
                    check_status(obj.to_json())
                    obj.print_item()

            elif args_values.action == "find":
                obj = Server(server_way).find(args_values.id, Category)
                check_status(obj)
                if obj is not None:
                    Note.show_table_headers()
                    for i in obj:
                        i.print_table()

            elif args_values.action == "clear":
                obj = Server(server_way).clear(args_values.id, Category)
                if obj is not None:
                    check_status(obj)

            elif args_values.action == "delete":
                obj = Server(server_way).delete(args_values.id, Category)
                if obj is not None:
                    check_status(obj)


    result(argument_parser(server_way))
