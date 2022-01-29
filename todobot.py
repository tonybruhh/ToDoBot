import json
import requests
import time
import urllib

from dbhelper import DBHelper


db = DBHelper()

TOKEN = '5054349266:AAGAHLTO1iyDXzqH7TGj1da32KA4mDK8f84'
URL = f'https://api.telegram.org/bot{TOKEN}/'


def get_url(url):
    response = requests.get(url)
    content = response.content.decode('utf8')
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + 'getUpdates?timeout=100'
    if offset:
        url += f'&offset={offset}'
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}&parse_mode=Markdown"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def handle_updates(updates):
    for update in updates['result']:
        try:
            text = update['message']['text']
            chat = update['message']['chat']['id']
            items = db.get_items(chat)

            if text == '/done':
                items = db.get_items(chat)
                if len(items) != 0:
                    keyboard = build_keyboard(items)
                    send_message('Select an item to delete', chat, keyboard)
                else:
                    send_message('The list is empty', chat)

            elif text == '/start':
                send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. "
                             "Send /done to remove items", chat)

            elif text.startswith('/'):
                continue

            elif text in items:
                db.delete_item(text, chat)
                items = db.get_items(chat)
                if len(items) != 0:
                    keyboard = build_keyboard(items)
                    send_message('Select an item to delete', chat, keyboard)
                else:
                    send_message('The list is empty', chat)

            elif text == '/list':
                items = db.get_items(chat)
                if len(items) != 0:
                    message = '\n'.join(items)
                    send_message(message, chat)
                else:
                    send_message('The list is empty, type anything you want to add', chat)


            else:
                db.add_item(text, chat)


        except KeyError:
            pass


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}
    return json.dumps(reply_markup)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates['result']) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

