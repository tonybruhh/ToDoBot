import telegram

from dbdriver import DBDriver

database = DBDriver()
database.setup()

class ToDoBot:

    class UserData:
        def __init__(self, text, chat_id, items):
            self.text = text
            self.chat_id = chat_id
            self.items = items

    def __init__(self, todo_queue):
        """ The data in queue contains tuples with the text of the message received from
         the user and user's chat id in (text, chat_id) format """
        self.queue = todo_queue
        self.calls = {
            '/list': self.call_list,
            '/done': self.call_delete_keyboard,
            '/start': self.call_start,
            '/clear': self.call_clear
        }

    def run(self):
        while not self.queue.empty():
            text, chat_id = self.queue.get()
            items = database.get_items(chat_id)
            userdata = self.UserData(text, chat_id, items)

            if userdata.text in self.calls:
                self.calls[userdata.text](userdata)

            elif userdata.text.startswith('/'):
                continue

            elif userdata.text in userdata.items:
                self.delete_item(userdata)

            else:
                database.add_item(userdata)


    def call_start(self, userdata):
        telegram.send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an"
                              " item. Send /done to remove items", userdata.chat_id)

    def call_list(self, userdata):
        if userdata.items:
            text_of_items = '\n'.join(userdata.items)
            telegram.send_message(text_of_items, userdata.chat_id)
        else:
            telegram.send_message('The list is empty, type anything you want to add', userdata.chat_id)

    def call_clear(self, userdata):
        if userdata.items:
            database.clear_items(userdata)
            telegram.send_message('The list has been cleared', userdata.chat_id)
        else:
            telegram.send_message('The list is empty', userdata.chat_id)

    def call_delete_keyboard(self, userdata):
        if userdata.items:
            keyboard = telegram.build_keyboard(userdata.items)
            telegram.send_message('Select an item to delete', userdata.chat_id, keyboard)
        else:
            telegram.send_message('The list is empty', userdata.chat_id)

    def delete_item(self, userdata):
        database.delete_item(userdata)
        userdata.items.remove(userdata.text)
        self.call_delete_keyboard(userdata)

