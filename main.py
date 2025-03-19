import os
import asyncio
from dotenv import load_dotenv  
from aiogram import Bot, Dispatcher
from models.database import Session
from models.models import User

from handlers import router
from utils.scheduler import scheduler, schedule_reminder


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN')) 
    dp = Dispatcher()
    dp.include_router(router)
    scheduler.start()
    session = Session()
    users = session.query(User).all()
    for user in users:
        if user.reminder_time:
            schedule_reminder(bot, user.user_id, user.reminder_time)
            
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')

