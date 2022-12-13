from telebot import types
from assets.string import *

CANCEL_BTN = types.KeyboardButton(CANCEL_STRING)

financial_aid_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton("Education")
financial_aid_markup.add(btn1, CANCEL_BTN)

race_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton("Chinese")
btn2 = types.KeyboardButton("Malay")
btn3 = types.KeyboardButton("Indian")
btn4 = types.KeyboardButton("Others")
race_markup.add(btn1, btn2, btn3, btn4, CANCEL_BTN)

gender_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton("Male")
btn2 = types.KeyboardButton("Female")
btn3 = types.KeyboardButton("Others")
gender_markup.add(btn1, btn2, btn3, CANCEL_BTN)

citizenship_status_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton("Singaporeans")
btn2 = types.KeyboardButton("PRs")
btn3 = types.KeyboardButton("Foreigners")
citizenship_status_markup.add(btn1, btn2, btn3, CANCEL_BTN)

monthly_household_income_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton("< $4000")
btn2 = types.KeyboardButton("$4000 - $6000")
btn3 = types.KeyboardButton("> $6000")
monthly_household_income_markup.add(btn1, btn2, btn3, CANCEL_BTN)

year_of_study_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton("Freshmore")
btn2 = types.KeyboardButton("Sophomore")
btn3 = types.KeyboardButton("Junior")
btn4 = types.KeyboardButton("Senior")
year_of_study_markup.add(btn1, btn2, btn3, btn4, CANCEL_BTN)

terms_and_conditions_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn1 = types.KeyboardButton(ACCEPT_STRING)
terms_and_conditions_markup.add(btn1, CANCEL_BTN)
