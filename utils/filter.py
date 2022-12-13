import telebot
from telebot import custom_filters


class IsValidGPA(custom_filters.SimpleCustomFilter):
    key = "valid_gpa"

    @staticmethod
    def check(message: telebot.types.Message):
        gpa = message.text
        try:
            gpa = float(gpa)
            return min(0, 5) <= gpa <= max(0, 5)
        except ValueError:
            return False


class IsAcceptedTermsAndConditions(custom_filters.SimpleCustomFilter):
    key = "accepted_terms_and_conditions"

    @staticmethod
    def check(message: telebot.types.Message):
        return True if message.text == "Accept" else False
