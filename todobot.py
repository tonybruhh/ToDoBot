import telegram

from dbhelper import DBHelper

db = DBHelper()
db.setup()


def handle_message(text, chat):
    try:
        items = db.get_items(chat)

        if text == '/done':
            items = db.get_items(chat)
            if len(items) != 0:
                keyboard = telegram.build_keyboard(items)
                telegram.send_message('Select an item to delete', chat, keyboard)
            else:
                telegram.send_message('The list is empty', chat)

        elif text == '/clear':
            items = db.get_items(chat)
            if len(items) != 0:
                db.clear_items(chat)
                telegram.send_message('The list has been cleared', chat)
            else:
                telegram.send_message('The list is empty', chat)

        elif text == '/start':
            telegram.send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an"
                                  " item. Send /done to remove items", chat)

        elif text == '/list':
            items = db.get_items(chat)
            if len(items) != 0:
                message = '\n'.join(items)
                telegram.send_message(message, chat)
            else:
                telegram.send_message('The list is empty, type anything you want to add', chat)

        elif text.startswith('/'):
            pass

        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            if len(items) != 0:
                keyboard = telegram.build_keyboard(items)
                telegram.send_message('Select an item to delete', chat, keyboard)
            else:
                telegram.send_message('The list is empty', chat)

        else:
            db.add_item(text, chat)

    except KeyError:
        pass
