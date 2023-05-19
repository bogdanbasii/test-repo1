import requests
import json
from core.utils import get_horoscope_by_day
from core.routes import ZODIAC_SIGNS


BOT_TOKEN = '5901762373:AAF5YvUzGor139zpNHZnWfQSBww38cQL_p8'
TG_BASE_URL = 'https://api.telegram.org/bot{}/'.format(BOT_TOKEN)


class User:
    def __init__(self, first_name, id, is_bot, language_code, username):
        self.first_name = first_name
        self.id = id
        self.is_bot = is_bot
        self.language_code = language_code
        self.username = username


class TelegramHandler:
    user = None
    text = None
    data = None

    def __init__(self, data):
        message = data.get('message')
        callback_query = data.get('callback_query')
        if message:
            self.chat_id = message['chat']['id']
            self.user = User(**message.get('from'))
            self.text = message.get('text')
        elif callback_query:
            self.chat_id = callback_query['message']['chat']['id']
            self.user = User(**callback_query.get('from'))
            self.data = callback_query.get('data')

    def handle_start(self):
        text = 'Hello, I am your horoscope bot. Please, choose your zodiac sign to get a prediction:'
        reply_markup = {
            "inline_keyboard": [
                [{"text": "Aquarius", "callback_data": "aquarius"}],
                [{"text": "Pisces", "callback_data": "pisces"}],
                [{"text": "Aries", "callback_data": "aries"}],
                [{"text": "Taurus", "callback_data": "taurus"}],
                [{"text": "Gemini", "callback_data": "gemini"}],
                [{"text": "Cancer", "callback_data": "cancer"}],
                [{"text": "Leo", "callback_data": "leo"}],
                [{"text": "Virgo", "callback_data": "virgo"}],
                [{"text": "Libra", "callback_data": "libra"}],
                [{"text": "Scorpio", "callback_data": "scorpio"}],
                [{"text": "Sagittarius", "callback_data": "sagittarius"}],
                [{"text": "Capricorn", "callback_data": "capricorn"}]
            ]
        }
        self.send_markupmessage(text, reply_markup)

    def send_markupmessage(self, text, reply_markup):
        data = {
            "chat_id": self.chat_id,
            "text": text,
            "reply_markup": json.dumps(reply_markup)
        }
        requests.post(f'{TG_BASE_URL}sendMessage', json=data)

    def handle(self):
        if self.text:
            text = self.text.lower()  # convert message text to lower case
            if text.startswith('/start'):
                self.handle_start()
        elif self.data:  # handle callback data
            if self.data == 'get_another_forecast':
                self.handle_start()
            else:
                horoscope = self.get_horoscope(self.data)
                self.send_message(horoscope)

    def send_message(self, text):
        reply_markup = {
            "inline_keyboard": [
                [{"text": "Get another forecast", "callback_data": "get_another_forecast"}]
            ]
        }
        data = {
            'chat_id': self.user.id,
            'text': text,
            'reply_markup': json.dumps(reply_markup)
        }
        requests.post(f'{TG_BASE_URL}sendMessage', json=data)

    def get_horoscope(self, sign):
        zodiac_num = ZODIAC_SIGNS[sign.capitalize()]
        horoscope = get_horoscope_by_day(zodiac_num, 'today')
        return horoscope
