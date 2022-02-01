import time

import todobot
import telegram


def main():
    last_update_id = None
    while True:
        text, chat = None, None
        updates = telegram.get_updates(last_update_id)
        print('1', updates)
        if len(updates['result']) > 0:
            last_update_id = telegram.get_last_update_id(updates) + 1
            text, chat = telegram.handle_updates(updates)
            if all([text, chat]):
                todobot.handle_message(text, chat)
        time.sleep(3)


if __name__ == '__main__':
    main()
