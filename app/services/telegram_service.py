import os, telebot

TELEGRAM_BOT = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])


@TELEGRAM_BOT.message_handler(func=lambda message: True)
def all_message(message):
  chat_id = message.chat.id
  user_message = message.text

  # data_transaction = handle_message_transaction(user_message)

  response_message = f"Received: {user_message}"
  TELEGRAM_BOT.send_message(chat_id, response_message)


def handle_message_transaction(message: str) -> object:
  pass


def run_polling_telegram():
  print("Starting bot")
  TELEGRAM_BOT.polling(none_stop=True, interval=1)


def stop_polling_telegram():
  print("Stoping bot")
  TELEGRAM_BOT.stop_bot()
