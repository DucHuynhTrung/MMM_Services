import os, asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from ..models import UserVisit
from ..services import handle_user_visit_bot_async

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN').__str__()
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def command_start(message: Message):
    current_datetime = datetime.now()
    user_visit = UserVisit(
        message.chat.id.__str__(), message.chat.first_name.__str__(), message.chat.last_name.__str__(),
        current_datetime, current_datetime, 1, False
    )

    # # Chạy xử lý DB bất đồng bộ đúng cách
    result = await handle_user_visit_bot_async(user_visit)

    message_str = f"Hi {user_visit.FirstName}, Tôi là bot hỗ trợ quản lý cho bạn.\nCảm ơn bạn đã ghé thăm." if result else "Xin lỗi, có lỗi xảy ra khi xử lý dữ liệu của bạn."
    await message.answer(message_str)


dp.message.register(command_start, Command("start"))


async def run_polling_telegram():
    """Chạy polling trong một task riêng biệt"""
    print("🚀 Starting Telegram bot...")
    loop = asyncio.get_running_loop()
    loop.create_task(dp.start_polling(bot))


async def stop_polling_telegram():
    """Dừng polling"""
    print("Stopping Telegram bot...")
    await dp.storage.close()
    await bot.session.close()
    print("🛑 Stopped Telegram bot")