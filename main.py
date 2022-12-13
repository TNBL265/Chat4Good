from src.fsm import bot

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
