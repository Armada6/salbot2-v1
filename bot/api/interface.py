from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError


class Iface:
    def __init__(self, host="127.0.0.1", port=28015, db="salbot"):
        self.r = RethinkDB()
        self.conn = self.r.connect(host=host, port=port, db=db)

    def clear_table(self, table: str):
        self.r.table(table).delete().run(self.conn)

    def create_table(self, table: str) -> bool:
        try:
            self.r.table_create(table).run(self.conn)
            return True
        except ReqlOpFailedError:
            return False

    def get_all(self, table: str) -> list:
        cursor = self.r.table(table).run(self.conn)
        docs = []
        for doc in cursor:
            docs.append(doc)
        return docs

    def get_by_uid(self, table: str, uid_name: str, uid_value: str) -> object:
        cursor = self.r.table(table).filter(self.r.row[uid_name] == uid_value).run(self.conn)
        for document in cursor:
            return document
        return None

    def insert(self, table: str, uid_name: str, uid_value: str, data: object) -> bool:
        if self.get_by_uid(table, uid_name, uid_value):
            return False
        data[uid_name] = uid_value
        self.r.table(table).insert(data).run(self.conn)
        return True

    def update(self, table: str, uid_name: str, uid_value: str, data: object) -> bool:
        if not self.get_by_uid(table, uid_name, uid_value):
            self.insert(table, uid_name, uid_value, data)
            return True
        self.r.table(table).filter(self.r.row[uid_name] == uid_value).update(data).run(self.conn)

    def delete(self, table: str, uid_name: str, uid_value: str):
        if not self.get_by_uid(table, uid_name, uid_value):
            return False
        self.r.table(table).filter(self.r.row[uid_name] == uid_value).delete().run(self.conn)

    def size(self, table: str):
        size = 0
        for item in self.r.table(table).run(self.conn):
            size += 1
        return size
