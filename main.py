import time

import todobot
import telegram


def main():
    last_update_id = None
    while True:
        updates = telegram.get_updates(last_update_id)
        print(updates)
        if len(updates['result']) > 0:
            last_update_id = telegram.get_last_update_id(updates) + 1
            todo_queue = telegram.handle_updates(updates)
            todobot.handle_message(todo_queue)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
