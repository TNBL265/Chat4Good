from telebot.handler_backends import BaseMiddleware

from .bot import bot
from .database import StatsDatabase
from assets.string import *
from utils.markup import DEFAULT_MARKUP


stats_db = StatsDatabase()


def collect_statistics(message):
    stats_db.local_data["user_id"] = message.from_user.id
    stats_db.local_data["username"] = message.from_user.username
    stats_db.local_data["max_steps"] += 1


def save_statistics(interaction_count):
    if stats_db.local_data:
        user_id = stats_db.local_data["user_id"]
        username = stats_db.local_data["username"]
        max_steps = stats_db.local_data["max_steps"]
        email = stats_db.local_data["email"]
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "max_steps": max_steps
        }
        stats_db.insert_user(user_data)
        stats_db.update_global_stats(interaction_count, user_id)


class Middleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ['message']

    def pre_process(self, message, data):
        if message.text == START_COMMAND:
            stats_db.reset_data()

    def post_process(self, message, data, exception):
        if exception:
            print(exception)
        elif message.text == NOT_READY or message.text == CANCEL:
            if message.text == CANCEL:
                save_statistics(interaction_count=message.message_id)
            bot.send_message(
                message.chat.id,
                f"Thank you, have a nice day! ☀️",
                reply_markup=DEFAULT_MARKUP
            )
            bot.delete_state(message.from_user.id, message.chat.id)
        elif message.text == EMAIL:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                stats_db.local_data["email"] = data[EMAIL]
            save_statistics(interaction_count=message.message_id)
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            collect_statistics(message)
            print(stats_db.local_data)


bot.setup_middleware(Middleware())
