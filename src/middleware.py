from telebot.handler_backends import BaseMiddleware

from .bot import bot
from .database import insert_user, update_global_stats
from assets.string import *


def collect_statistics(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data:
            stats = data.get("stats", None)
            if not stats:
                data["stats"] = {
                    "user_id": message.from_user.id,
                    "username": message.from_user.username,
                    "max_steps": len(data),
                }
            else:
                stats["max_steps"] = max(stats["max_steps"], len(data))


class Middleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ['message']
        self.stats = None

    def pre_process(self, message, data):
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if data:
                    self.stats = data.get("stats", None)
        except KeyError:
            pass

        if message.text == CANCEL_STRING:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, "All your information has been reset. Press /start to try again.")

    def post_process(self, message, data, exception):
        if exception:
            print(exception)
        elif message.text == CANCEL_STRING or message.text == ACCEPT_STRING:
            print("Saving statistics")
            if self.stats:
                user_id = self.stats["user_id"]
                username = self.stats["username"]
                max_steps = self.stats["max_steps"]
                interaction_count = message.message_id

                # Insert/Update mongodb
                insert_user(user_id, username, max_steps)
                update_global_stats(interaction_count, user_id)

        else:
            collect_statistics(message)


bot.setup_middleware(Middleware())
