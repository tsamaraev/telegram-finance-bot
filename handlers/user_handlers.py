from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from models.crud import get_user
from models.database import Session

router = Router()


@router.message(CommandStart())
async def greet_user(message: Message):
    await message.answer("Привет! Как я могу помочь вам сегодня?")
    # Создаем сессию
    session = Session()
    # Получаем пользователя
    user = get_user(session, user_id=message.from_user.id)
    # Закрываем сессию
    session.close()
    if user:
        await message.answer(f"Ваш баланс: {user}")
    else:
        await message.answer("Пользователь не найден.")
