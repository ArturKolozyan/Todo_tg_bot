import asyncio
import logging
from aiogram import Bot, Dispatcher
# import datetime
# from aiogram.utils.formatting import as_list

from app.handlers import router
from config import BOT_TOKEN

from db.db import create_db_and_tables

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


# async def send_reminders():
#     """
#     Функция для отправки напоминаний
#     """
#     while True:
#         now = datetime.datetime.now()
#         current_time_str = now.strftime("%H:%M")
#         for user_id, tasks in user_tasks.items():
#             reminder_time = user_reminder_times.get(user_id)
#             if reminder_time == current_time_str:
#                 task_messages = [f"- {task['task']}" for task in tasks]
#                 message_text = f"⏰ Напоминание!\nВаши задачи на сегодня:\n{as_list(*task_messages)}"
#                 await bot.send_message(user_id, message_text)
#         await asyncio.sleep(60)


async def on_startup():
    await create_db_and_tables()
    print("Bot started")

async def main():
    dp.startup.register(on_startup)
    logging.basicConfig(level=logging.INFO)
    # asyncio.create_task(send_reminders())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
