import os, telebot

TELEGRAM_BOT = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])


@TELEGRAM_BOT.message_handler(commands=['start'])
def command_start(message):
  chat_id = message.chat.id
  TELEGRAM_BOT.send_message(chat_id, "Hi!")


@TELEGRAM_BOT.message_handler(commands=['help'])
def command_help(message):
  chat_id = message.chat.id
  TELEGRAM_BOT.send_message(chat_id, "Help!")


@TELEGRAM_BOT.message_handler(commands=['chi'])
def command_help(message):
  chat_id = message.chat.id
  TELEGRAM_BOT.send_message(chat_id, "Help!")


@TELEGRAM_BOT.message_handler(func=lambda message: True)
def all_message(message):
  chat_id = message.chat.id
  user_message = message.text

  if user_message == "/chi":
    ask = TELEGRAM_BOT.send_message(chat_id,
                                    "Được rồi bạn đã chi tiêu gì nào?")
    TELEGRAM_BOT.register_next_step_handler(ask, handle_message_transaction)


def handle_message_transaction(message: str):
  data: object = {}
  if message == "/chi":
    data = handle_expenditure(message)
  elif message == "/thu":
    data = handle_income(message)

  if data != {}:
    handle_database(data)


def handle_expenditure(message: str) -> object:
  pass


def handle_income(message: str) -> object:
  pass


def handle_database(data: object):
  pass


def run_polling_telegram():
  print("Starting bot")
  TELEGRAM_BOT.polling(none_stop=True, interval=1)


def stop_polling_telegram():
  print("Stoping bot")
  TELEGRAM_BOT.stop_bot()
