import telegram

from dbhelper import DBHelper

db = DBHelper()
db.setup()


# def func_dict_initiator(command):
#     def func_dict_decorator(method):
#         def wrapper(self, text, chat, items):
#             method(self, text, chat, items)
#
#         return wrapper
#
#     return func_dict_decorator


class ToDoBot:

    def __init__(self, todo_queue):
        self.queue = todo_queue
        self.calls = dict()

    def func_dict_initiator(chat_command):
        def func_dict_decorator(method):
            def wrapper(self, text, chat, items):
                self.calls[chat_command] = method
                method(self, text, chat, items)

            return wrapper

        return func_dict_decorator

    def run(self):
        queue_size = self.queue.qsize()
        for _ in range(queue_size):
            text, chat = self.queue.get()
            items = db.get_items(chat)
            if text in self.calls:
                self.calls[text](text, chat, items)
            elif text.startswith('/'):
                continue
            elif text in items:
                self.delete_item(text, chat, items)
            else:
                db.add_item(text, chat)

    @func_dict_initiator('/list')
    def call_list(self, text, chat, items):
        if len(items) != 0:
            message = '\n'.join(items)
            telegram.send_message(message, chat)
        else:
            telegram.send_message('The list is empty, type anything you want to add', chat)

    def call_delete(self, text, chat, items):
        if len(items) != 0:
            keyboard = telegram.build_keyboard(items)
            telegram.send_message('Select an item to delete', chat, keyboard)
        else:
            telegram.send_message('The list is empty', chat)

    def call_clear(self, text, chat, items):
        if len(items) != 0:
            db.clear_items(chat)
            telegram.send_message('The list has been cleared', chat)
        else:
            telegram.send_message('The list is empty', chat)

    def call_start(self, text, chat, items):
        telegram.send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an"
                              " item. Send /done to remove items", chat)

    def delete_item(self, text, chat, items):
        db.delete_item(text, chat)
        items = db.get_items(chat)
        self.call_delete(text, chat, items)

a = ToDoBot()