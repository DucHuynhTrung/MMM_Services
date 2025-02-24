import os, telebot
from dotenv import load_dotenv
from ..utils import handle_message_income, handle_message_expenditure, handle_message_credit

load_dotenv()
TELEGRAM_BOT = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))


@TELEGRAM_BOT.message_handler(commands=['start'])
def command_start(message):
  chat_id = message.chat.id
  first_name = message.chat.first_name
  TELEGRAM_BOT.send_message(
      chat_id, f"Hi {first_name}, Tôi là bot hỗ trợ quản lý cho bạn.")
  ask_cash = TELEGRAM_BOT.send_message(
      chat_id,
      f"Hãy cho tôi biết tổng tiền bạn đang có theo cấu trúc sau: \n'tiền mặt, tiền ngân hàng (tất cả ngân hàng), hạn mức tín dụng, số tiền tín dụng khả dụng, số tiền nợ"
  )
  TELEGRAM_BOT.register_next_step_handler(ask_cash, handle_start)


@TELEGRAM_BOT.message_handler(commands=['chi'])
def command_chi(message):
  chat_id = message.chat.id

  ask = TELEGRAM_BOT.send_message(chat_id, "Được rồi bạn đã chi tiêu gì nào?")
  TELEGRAM_BOT.register_next_step_handler(ask, handle_expenditure)


@TELEGRAM_BOT.message_handler(commands=['thu'])
def command_thu(message):
  pass


@TELEGRAM_BOT.message_handler(commands=['tindung'])
def command_tindung(message):
  pass


@TELEGRAM_BOT.message_handler(commands=['tratindung'])
def command_tratindung(message):
  pass


@TELEGRAM_BOT.message_handler(func=lambda message: True)
def all_message(message):
  chat_id = message.chat.id
  user_message = message.text

  TELEGRAM_BOT.send_message(chat_id, user_message)


def handle_start(message):
  chat_id = message.chat.id
  cash, bank, credit, available_credit, debt = [0, 0, 0, 0, 0]
  try:
    cash, bank, credit, available_credit, debt = [
        float(i) for i in message.text.split(", ")
    ]

    data: object = {
        type: "start",
        cash: cash,
        bank: bank,
        credit: credit,
        available_credit: available_credit,
        debt: debt
    }
    handle_database(data)

  except:
    TELEGRAM_BOT.send_message(
        chat_id,
        "Error 101: Quá trình phần tích đã xảy ra lỗi. Vui lòng thử lại bằng cách bấm lệnh /start"
    )


def handle_expenditure(message: str):
  pass


def handle_income(message: str):
  pass


def handle_database(data: object):
  pass


def run_polling_telegram():
  print("Starting bot")
  TELEGRAM_BOT.polling(none_stop=False, interval=1)


def stop_polling_telegram():
  print("Stoping bot")
  TELEGRAM_BOT.stop_bot()
