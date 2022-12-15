import re

import telebot
from telebot import custom_filters

from assets.string import CANCEL


def is_not_canceled(message):
    return message.text != CANCEL


class IsValidEmail(custom_filters.SimpleCustomFilter):
    key = "valid_email"

    @staticmethod
    def check(message: telebot.types.Message):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, message.text):
            return True
        return False
