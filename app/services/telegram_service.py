import os, telebot, asyncio
from datetime import datetime
from dotenv import load_dotenv
from ..utils import handle_message_income, handle_message_expenditure
from ..db import handle_user_visit_bot_async
from ..models import UserVisit

load_dotenv()
TELEGRAM_BOT = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN').__str__())


@TELEGRAM_BOT.message_handler(commands=['start'])
async def command_start(message):
  current_datetime = datetime.now()
  user_visit = UserVisit(message.chat.id, message.chat.first_name, message.chat.last_name, current_datetime, current_datetime, 1, False)
  result = await handle_user_visit_bot_async(user_visit)

  TELEGRAM_BOT.send_message(user_visit.ID, f"Hi {user_visit.FirstName}, Tôi là bot hỗ trợ quản lý cho bạn.")
  # gửi link đăng nhập bằng google
  

  # ask_cash = TELEGRAM_BOT.send_message(
  #     user_visit.ID,
  #     f"Hãy cho tôi biết tổng tiền bạn đang có theo cấu trúc sau: \n'tiền mặt, tiền ngân hàng (tất cả ngân hàng), hạn mức tín dụng, số tiền tín dụng khả dụng, số tiền nợ"
  # )
  # TELEGRAM_BOT.register_next_step_handler(ask_cash, handle_start)


@TELEGRAM_BOT.message_handler(commands=['chi'])
def command_chi(message):
  chat_id = message.chat.id

  ask = TELEGRAM_BOT.send_message(chat_id, "Được rồi bạn đã chi tiêu gì nào?")
  TELEGRAM_BOT.register_next_step_handler(ask, handle_expenditure)


@TELEGRAM_BOT.message_handler(commands=['thu'])
def command_thu(message):
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
  print("🔄 Bot Telegram đang chạy...")
  TELEGRAM_BOT.infinity_polling(timeout=10, long_polling_timeout=5)

def stop_polling_telegram():
  print("🔴 Đang dừng bot...")
  TELEGRAM_BOT.stop_bot()
  print("⏹ Bot Telegram đã dừng.")



