from telebot.handler_backends import State, StatesGroup

from .middleware import bot
from utils.markup import *
from utils.filter import *
from assets.string import *


class C4G(StatesGroup):
    financial_aid_scheme = State()
    race = State()
    gender = State()
    citizenship_status = State()
    family_members = State()
    monthly_household_income = State()
    year_of_study = State()
    gpa = State()
    result = State()


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.set_state(message.from_user.id, C4G.financial_aid_scheme, message.chat.id)
    bot.send_message(
        message.chat.id,
        "What type of financial assistance scheme are you looking for?",
        reply_markup=financial_aid_markup
    )


@bot.message_handler(state=C4G.financial_aid_scheme)
def get_financial_aid_scheme(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["financial_aid_scheme"] = message.text
    bot.set_state(message.from_user.id, C4G.race, message.chat.id)
    bot.send_message(
        message.chat.id,
        "What is your race?",
        reply_markup=race_markup
    )


@bot.message_handler(state=C4G.race)
def get_race(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["race"] = message.text
    bot.set_state(message.from_user.id, C4G.gender, message.chat.id)
    bot.send_message(
        message.chat.id,
        "What is your gender?",
        reply_markup=gender_markup
    )


@bot.message_handler(state=C4G.gender)
def get_gender(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["gender"] = message.text
    bot.set_state(message.from_user.id, C4G.citizenship_status, message.chat.id)
    bot.send_message(
        message.chat.id,
        "What is your citizenship status?",
        reply_markup=citizenship_status_markup
    )


@bot.message_handler(state=C4G.citizenship_status)
def get_citizenship_status(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["citizenship_status"] = message.text
    bot.set_state(message.from_user.id, C4G.family_members, message.chat.id)
    bot.send_message(
        message.chat.id,
        "How many family members do you have?"
    )


@bot.message_handler(state=C4G.family_members, is_digit=True)
def get_family_members(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["family_members"] = message.text
    bot.set_state(message.from_user.id, C4G.monthly_household_income, message.chat.id)
    bot.send_message(
        message.chat.id,
        "What is your monthly household income?",
        reply_markup=monthly_household_income_markup
    )


@bot.message_handler(state=C4G.family_members, is_digit=False)
def age_incorrect(message):
    bot.send_message(message.chat.id, "Please enter a number")


@bot.message_handler(state=C4G.monthly_household_income)
def get_monthly_household_income(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["monthly_household_income"] = message.text
    bot.set_state(message.from_user.id, C4G.year_of_study, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Which year of study are you in?",
        reply_markup=year_of_study_markup
    )


@bot.message_handler(state=C4G.year_of_study)
def get_year_of_study(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["year_of_study"] = message.text
    bot.set_state(message.from_user.id, C4G.gpa, message.chat.id)
    bot.send_message(
        message.chat.id,
        "What is your current gpa (out of 5.0)?"
    )


@bot.message_handler(state=C4G.gpa, valid_gpa=True)
def get_gpa(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["gpa"] = message.text
    bot.set_state(message.from_user.id, C4G.result, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Please read our T&C",
        reply_markup=terms_and_conditions_markup
    )


@bot.message_handler(state=C4G.gpa, valid_gpa=False)
def gpa_incorrect(message):
    bot.send_message(message.chat.id, "Please enter a value between 0 and 5")


@bot.message_handler(state=C4G.result, func=lambda message: message.text == ACCEPT_STRING)
def get_result(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        monthly_household_income = data['monthly_household_income']
        family_members = int(data['family_members'])
        lo = str(round(4000/family_members, 2))
        hi = str(round(6000/family_members, 2))
        if monthly_household_income == "< $4000":
            monthly_per_capita_income = "< $" + lo
        elif monthly_household_income == "$4000 - $6000":
            monthly_per_capita_income = "$" + lo + " - " + "$" + hi
        elif monthly_household_income == "> $6000":
            monthly_per_capita_income = "> $" + hi
        else:
            monthly_per_capita_income = "fl4g"

        msg = (
            f"""
Here are the information we have collected:

- Financial Aid Scheme: {data['financial_aid_scheme']}
- Race: {data['race']}
- Gender: {data['gender']}
- Citizenship: {data['citizenship_status']}
- Family Members: {family_members}
- Monthly Household Income: {monthly_household_income}
- Monthly Per Capita Income: {monthly_per_capita_income}
- Year of Study: {data['year_of_study']}
- GPA: {data['gpa']}"""
        )
        bot.send_message(
            message.chat.id,
            msg
        )
    bot.delete_state(message.from_user.id, message.chat.id)


# built-in filter
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

# custom filter from validator.py
bot.add_custom_filter(IsValidGPA())
bot.add_custom_filter(IsAcceptedTermsAndConditions())
