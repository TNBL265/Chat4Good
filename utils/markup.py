from telebot import types
from assets.string import *

CANCEL_BTN = types.KeyboardButton(CANCEL)

KEYBOARD_ARGS = {"one_time_keyboard": True, "resize_keyboard": True}
DEFAULT_MARKUP = types.ReplyKeyboardMarkup(**KEYBOARD_ARGS).add(*[START_COMMAND, CONTACT_COMMAND])
READY_MARKUP = types.ReplyKeyboardMarkup(**KEYBOARD_ARGS).add(*[READY, NOT_READY])


def create_markup(options):
    markup = types.ReplyKeyboardMarkup(**KEYBOARD_ARGS)
    options = options.split("; ")

    btns = []
    for option in options:
        btns.append(types.KeyboardButton(option))
    btns.append(CANCEL_BTN)

    markup.add(*btns)
    return markup


