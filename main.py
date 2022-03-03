import time

from todobot import ToDoBot
import telegram


def main():
    last_update_id = None
    while True:
        updates = telegram.get_updates(last_update_id)
        print(updates)
        if len(updates['result']) > 0:
            last_update_id = telegram.get_last_update_id(updates) + 1
            queue = telegram.handle_updates(updates)
            todolist = ToDoBot(queue)
            todolist.run()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
