from telebot.handler_backends import State, StatesGroup
from telebot.formatting import hbold, hitalic, hunderline

from .middleware import bot
from .database import ScholarshipAndFinancialAidDatabase
from utils.markup import *
from utils.filter import *
from assets.string import *


safa_db = ScholarshipAndFinancialAidDatabase("assets/csv/SUTD_safa.csv")


class C4G(StatesGroup):
    start = State()
    citizenship_status = State()
    gender = State()
    race = State()
    per_capita_income = State()
    year_of_study = State()
    pillar = State()
    email = State()


@bot.message_handler(commands=["start"])
def ready(message):
    safa_db.populate_data()
    bot.set_state(message.from_user.id, C4G.start, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"""
Hi there @{message.from_user.username}! Nice to meet you! We are here to provide recommendations for scholarships and \
financial aid schemes based on your eligibility 📝
        
Are you ready?
        """,
        reply_markup=READY_MARKUP
    )


@bot.message_handler(state=C4G.start, func=lambda message: message.text == READY)
def start_command(message):
    safa_db.populate_data()
    bot.set_state(message.from_user.id, C4G.citizenship_status, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"""
Great! To provide you with personalised recommendations, we would like you to answer a few short questions \
about yourself.

Rest assured that all data collected will be held anonymously and securely.

{hbold("‼️ Please enter your SUTD email once you have completed all the questions in order for you to be eligible to win SGD $5 💸.")} 
        """,
        parse_mode="HTML"
    )
    bot.send_message(
        message.chat.id,
        f"{hbold('Q1.')} What is your citizenship status?",
        reply_markup=create_markup(safa_db.columns[CITIZENSHIP_STATUS]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.citizenship_status, func=is_not_canceled)
def get_citizenship_status(message):
    safa_db.narrow_down_safa_options(criteria=CITIZENSHIP_STATUS, text=message.text)
    bot.set_state(message.from_user.id, C4G.gender, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hbold('Q2.')} What is your gender?",
        reply_markup=create_markup(safa_db.columns[GENDER]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.gender, func=is_not_canceled)
def get_gender(message):
    safa_db.narrow_down_safa_options(criteria=GENDER, text=message.text)
    bot.set_state(message.from_user.id, C4G.race, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hbold('Q3.')} What is your race?",
        reply_markup=create_markup(safa_db.columns[RACE]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.race, func=is_not_canceled)
def get_race(message):
    safa_db.narrow_down_safa_options(criteria=RACE, text=message.text)
    bot.set_state(message.from_user.id, C4G.per_capita_income, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hbold('Q4.')} What is your monthly household income per capita?",
        reply_markup=create_markup(safa_db.columns[PCI]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.per_capita_income, func=is_not_canceled)
def get_monthly_household_income(message):
    safa_db.narrow_down_safa_options(criteria=PCI, text=message.text)
    bot.set_state(message.from_user.id, C4G.year_of_study, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hbold('Q5.')} Which year of study are you currently in?",
        reply_markup=create_markup(safa_db.columns[YEAR_OF_STUDY]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.year_of_study, func=is_not_canceled)
def get_year_of_study(message):
    safa_db.narrow_down_safa_options(criteria=YEAR_OF_STUDY, text=message.text)
    bot.set_state(message.from_user.id, C4G.pillar, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hbold('Q6.')} Which pillar are you currently in or intending to pursue?",
        reply_markup=create_markup(safa_db.columns[PILLAR]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.pillar, func=is_not_canceled)
def get_pillar(message):
    safa_db.narrow_down_safa_options(criteria=PILLAR, text=message.text)
    bot.send_message(
        message.chat.id,
        f"""
Thank you for your responses, @{message.from_user.username}!

Here is a list of recommendations we have come up with:

{safa_db.format_safa_output()}
        """,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    bot.send_message(
        message.chat.id,
        f"""
We hope that this list is helpful for you 😊 Feel free to reach out to us if you have any feedback or suggestions!

{hbold("‼️ Enter your SUTD email now to stand a chance to win SGD $5 💸.")} 

Do read the T&C in the email we sent earlier 📝. 
        """,
        parse_mode="HTML"
    )
    bot.set_state(message.from_user.id, C4G.email, message.chat.id)


@bot.message_handler(state=C4G.email, valid_email=True, func=is_not_canceled)
def get_email(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data[EMAIL] = message.text
    message.text = EMAIL
    bot.send_message(
        message.chat.id,
        "Thank you for interacting with us! You will be contacted via email should you win the prize.",
        reply_markup=DEFAULT_MARKUP
    )


@bot.message_handler(state=C4G.email, valid_email=False, func=is_not_canceled)
def gpa_incorrect(message):
    bot.send_message(message.chat.id, "Invalid email")


# built-in filter
bot.add_custom_filter(custom_filters.StateFilter(bot))

# custom filter from validator.py
bot.add_custom_filter(IsValidEmail())