from argparse_methods import argument_parser
from methods import create_request, unite_txt, check_for_errors

"""Default server"""

server_way = 'http://127.0.0.1:5000'


class Category:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @staticmethod
    def request_name():
        return "category"

    @staticmethod
    def from_json(resp):
        if "message" in resp:
            print('status - ' + resp["status"], "---", resp["message"])
        else:
            return Category(resp["id"], resp['name'])

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


class Note:
    def __init__(self, id=None, record=None, category=None):
        self.id = id
        self.record = record
        self.category = category

    @staticmethod
    def request_name():
        return "note"

    @staticmethod
    def from_json(resp):
        if "message" in resp:
            print('status - ' + resp["status"], "---", resp["message"])
        else:
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
        print("{:1} {:2} {:.50} {:1} {:2} {:1}".format("|", self.id, self.record.center(50, "."), "|",
                                                       self.category["name"], self.category["id"]))


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
            return item.from_json(resp.json())

    def find(self, item):
        if item.request_name() == "note":
            resp = check_for_errors(self._send_request(item.request_name(), "find", item.to_json()))
            if resp is not None:
                item_list = []
                for i in resp.json()["data"]:
                    item_list.append(Note.from_json(i))
                return item_list
        elif item.request_name() == "category":
            resp = check_for_errors(self._send_request(item.request_name(), "find-note", item.to_json()))
            if resp is not None:
                item_list = []
                for i in resp.json()["data"]:
                    item_list.append(Note.from_json(i))

                return item_list

    def delete(self, item):
        resp = check_for_errors(self._send_request(item.request_name(), "delete", item.to_json()))
        if resp is not None:
            return item.from_json(resp.json())

    def clear(self, item):
        resp = check_for_errors(self._send_request(item.request_name(), "clear", item.to_json()))
        if resp is not None:
            return item.from_json(resp.json())


if __name__ == '__main__':
    # Processing requests
    def result(args_values):
        if args_values.object == "category":
            if args_values.action == "add":
                obj = Server(server_way).add(Category(0, unite_txt(args_values.text)))
                if obj is not None:
                    obj.print_item()
            elif args_values.action == "list":
                obj = Server(server_way).list(Category)
                for i in obj:
                    i.print_table()
            elif args_values.action == "change":
                obj = Server(server_way).change(Category(args_values.id, unite_txt(args_values.text)))
                obj.print_item()
            elif args_values.action == "find":
                obj = Server(server_way).find(Category(args_values.id, 0))
                if obj is not None:
                    for i in obj:
                        i.print_table()
            elif args_values.action == "clear":
                Server(server_way).clear(Category(args_values.id, 0))
            elif args_values.action == "delete":
                Server(server_way).delete(Category(args_values.id, 0))
        elif args_values.object == "note":
            if args_values.action == "add":
                obj = Server(server_way).add(Note(0, unite_txt(args_values.text), args_values.category))
                obj.print_item()
            elif args_values.action == "list":
                obj = Server(server_way).list(Note(0, 0, 0))
                for i in obj:
                    i.print_table()
            elif args_values.action == "change":
                Server(server_way).change(Note(args_values.id, unite_txt(args_values.text), args_values.category))
            elif args_values.action == "find":
                obj = Server(server_way).find(Note(0, unite_txt(args_values.text), 0))
                if obj is not None:
                    for i in obj:
                        i.print_table()
            elif args_values.action == "delete":
                Server(server_way).delete(Note(args_values.id, 0, 0))


    result(argument_parser(server_way))
