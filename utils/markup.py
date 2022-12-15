from telebot import types
from assets.string import *

CANCEL_BTN = types.KeyboardButton(CANCEL)

DEFAULT_MARKUP = types.ReplyKeyboardMarkup(one_time_keyboard=True).add(START_COMMAND)
READY_MARKUP = types.ReplyKeyboardMarkup(one_time_keyboard=True).add(*[READY, NOT_READY])


def create_markup(options):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = options.split("; ")

    btns = []
    for option in options:
        btns.append(types.KeyboardButton(option))
    btns.append(CANCEL_BTN)

    markup.add(*btns)
    return markup


