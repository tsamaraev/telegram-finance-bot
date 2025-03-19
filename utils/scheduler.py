from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from models.crud import get_user
from models.database import Session

scheduler = AsyncIOScheduler()

async def send_reminder(bot: Bot, user_id: int):
    """Отправка напоминания пользователю"""
    try:
        await bot.send_message(user_id, "Не забудьте внести ваши сегодняшние расходы/доходы! 📝")
    except Exception as e:
        print(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")

def schedule_reminder(bot: Bot, user_id: int, reminder_time: str):
    """Планирование напоминания для пользователя"""
    # Преобразуем время в формат часы:минуты
    # Заменяем нижнее подчеркивание на двоеточие, если оно присутствует
    reminder_time = reminder_time.replace('_', ':')
    hours, minutes = reminder_time.split(':')
    
    # Создаем задачу с ежедневным напоминанием в указанное время
    scheduler.add_job(
        send_reminder,
        trigger=CronTrigger(hour=hours, minute=minutes),
        args=[bot, user_id],
        id=f"reminder_{user_id}",
        replace_existing=True
    )

def remove_reminder(user_id: int):
    """Удаление напоминания для пользователя"""
    try:
        scheduler.remove_job(f"reminder_{user_id}")
    except:
        pass