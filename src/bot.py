import os
import telebot
from telebot.storage import StateMemoryStorage

# FSM storage
state_storage = StateMemoryStorage()

# Our bot
bot = telebot.TeleBot(
    os.environ["TELEBOT_API_TOKEN"],
    state_storage=state_storage,
    use_class_middlewares=True
)
