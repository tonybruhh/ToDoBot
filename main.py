import todobot
import time


def main():
    last_update_id = None
    while True:
        updates = todobot.get_updates(last_update_id)
        if len(updates['result']) > 0:
            last_update_id = todobot.get_last_update_id(updates) + 1
            todobot.handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
