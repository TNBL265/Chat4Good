from telebot.handler_backends import State, StatesGroup
from telebot.formatting import hunderline

from .middleware import bot
from .database import ScholarshipAndFinancialAidDatabase, StatsDatabase
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
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data[STATISTICS] = StatsDatabase.reset_data()
        data[STATISTICS][USER_ID] = message.from_user.id
        data[STATISTICS][USERNAME] = message.from_user.username
    bot.set_state(message.from_user.id, C4G.citizenship_status, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"""
Great! To provide you with personalised recommendations, we would like you to answer a few short questions \
about yourself. 
        """
    )
    bot.send_message(
        message.chat.id,
        f"{hunderline('Q1.')} What is your citizenship status?",
        reply_markup=create_markup(ScholarshipAndFinancialAidDatabase.columns[CITIZENSHIP_STATUS]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.citizenship_status, func=is_not_canceled)
def get_citizenship_status(message):
    safa_db.narrow_down_safa_options(criteria=CITIZENSHIP_STATUS, text=message.text)
    bot.set_state(message.from_user.id, C4G.gender, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hunderline('Q2.')} What is your gender?",
        reply_markup=create_markup(ScholarshipAndFinancialAidDatabase.columns[GENDER]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.gender, func=is_not_canceled)
def get_gender(message):
    safa_db.narrow_down_safa_options(criteria=GENDER, text=message.text)
    bot.set_state(message.from_user.id, C4G.race, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hunderline('Q3.')} What is your race?",
        reply_markup=create_markup(ScholarshipAndFinancialAidDatabase.columns[RACE]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.race, func=is_not_canceled)
def get_race(message):
    safa_db.narrow_down_safa_options(criteria=RACE, text=message.text)
    bot.set_state(message.from_user.id, C4G.per_capita_income, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hunderline('Q4.')} What is your monthly household income per capita?",
        reply_markup=create_markup(ScholarshipAndFinancialAidDatabase.columns[PCI]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.per_capita_income, func=is_not_canceled)
def get_monthly_household_income(message):
    safa_db.narrow_down_safa_options(criteria=PCI, text=message.text)
    bot.set_state(message.from_user.id, C4G.year_of_study, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"""
{hunderline('Q5.')} Which year of study are you currently in?
Term 1-2 : Freshmore
Term 3-4: Sophomore
Term 5-6: Junior
Term 7-8: Senior
        """,
        reply_markup=create_markup(ScholarshipAndFinancialAidDatabase.columns[YEAR_OF_STUDY]),
        parse_mode="HTML"
    )


@bot.message_handler(state=C4G.year_of_study, func=is_not_canceled)
def get_year_of_study(message):
    safa_db.narrow_down_safa_options(criteria=YEAR_OF_STUDY, text=message.text)
    bot.set_state(message.from_user.id, C4G.pillar, message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{hunderline('Q6.')} Which pillar are you currently in or intending to pursue?",
        reply_markup=create_markup(ScholarshipAndFinancialAidDatabase.columns[PILLAR]),
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
We hope that this list is helpful for you 😊 Feel free to /contact us if you have any feedback or suggestions!
        """,
        reply_markup=DEFAULT_MARKUP
    )


@bot.message_handler(commands=["contact"])
def contact(message):
    bot.send_message(
        message.chat.id,
        f"""
Hope our @Chat4Good bot has been serving you well so far. 
It is in heavy development, so any feedback will be greatly appreciated!
 
@weeotim: Business Development
@jodesloads: UI/UX/Product Design
@BlongTran: Main Dev (for now)
@joelwh: Main Dev (soon)
@rktmeister: Cybersecurity Specialist
        """,
        reply_markup=DEFAULT_MARKUP
    )


# built-in filter
bot.add_custom_filter(custom_filters.StateFilter(bot))
