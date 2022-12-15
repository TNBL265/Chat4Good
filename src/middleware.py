from telebot.handler_backends import BaseMiddleware

from .bot import bot
from .database import StatsDatabase, ScholarshipAndFinancialAidDatabase
from assets.string import *
from utils.markup import DEFAULT_MARKUP

stats_db = StatsDatabase()
STEPS_CAP = 7


def save_statistics(data):
    if data:
        stats_db.insert_user(data)


class Middleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ["message"]

    def pre_process(self, message, data):
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if not data:
                    return
                value = message.text
                if value != CANCEL:
                    # Store user's input
                    for k, v in ScholarshipAndFinancialAidDatabase.columns.items():
                        if value in v:
                            data[STATISTICS][k] = value
                            break
        except KeyError:
            pass

    def post_process(self, message, data, exception):
        if exception:
            print("Exception: ", exception)
            return
        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if not data:
                    return
                if message.text == NOT_READY or message.text == CANCEL:
                    # Early stopping
                    if message.text == CANCEL:
                        save_statistics(data[STATISTICS])
                    bot.send_message(
                        message.chat.id,
                        f"Thank you, have a nice day! ☀️",
                        reply_markup=DEFAULT_MARKUP
                    )
                    bot.delete_state(message.from_user.id, message.chat.id)
                elif message.text != CONTACT_COMMAND:
                    # As long as not /contact we will count
                    # Save stats after every step
                    data[STATISTICS][MAX_STEPS] += 1
                    if data[STATISTICS][MAX_STEPS] == 1 or data[STATISTICS][MAX_STEPS] >= STEPS_CAP:
                        print(f"Checkpoint for {message.from_user.username}", data[STATISTICS])
                    save_statistics(data[STATISTICS])

                    # Last state then delete data after saving
                    if message.text in ScholarshipAndFinancialAidDatabase.columns[PILLAR]:
                        bot.delete_state(message.from_user.id, message.chat.id)
        except KeyError:
            pass

bot.setup_middleware(Middleware())
