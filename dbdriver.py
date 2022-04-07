import sqlite3


class DBDriver:
    def __init__(self, dbname='todo.sqlite'):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname)

    def setup(self):
        print('creating table')
        creating_table = 'CREATE TABLE IF NOT EXISTS items (description text, user text)'
        creating_item_id = 'CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)'
        creating_user_id = 'CREATE INDEX IF NOT EXISTS ownIndex ON items (user ASC)'
        self.connection.execute(creating_table)
        self.connection.execute(creating_item_id)
        self.connection.execute(creating_user_id)
        self.connection.commit()

    def add_item(self, userdata):
        inserting = 'INSERT INTO items (description, user) VALUES (?, ?)'
        item_text = userdata.text
        user = userdata.chat_id
        args = (item_text, user)
        self.connection.execute(inserting, args)
        self.connection.commit()

    def delete_item(self, userdata):
        deleting = 'DELETE FROM items WHERE description = (?) AND user = (?)'
        item_text = userdata.text
        user = userdata.chat_id
        args = (item_text, user)
        self.connection.execute(deleting, args)
        self.connection.commit()

    def get_items(self, user):
        selecting = 'SELECT description FROM items WHERE user = (?)'
        args = (user,)
        return [x[0] for x in self.connection.execute(selecting, args)]

    def clear_items(self, userdata):
        deleting = 'DELETE FROM items WHERE user = (?)'
        user = userdata.chat_id
        args = (user,)
        self.connection.execute(deleting, args)
        self.connection.commit()
