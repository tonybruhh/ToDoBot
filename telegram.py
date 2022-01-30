import json
import requests
import urllib


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


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}&parse_mode=Markdown"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}
    return json.dumps(reply_markup)