from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline_keyboard import start_register_keyboard, currency_keyboard, reminder_keyboard, get_settings_keyboard, get_reminder_times_keyboard
from models.database import Session
from models.crud import create_user, get_user, get_user_by_username, update_user
from utils.messages import WELCOME_MESSAGE, REGISTER_MESSAGE
from states.user_states import RegisterStates
from utils.scheduler import schedule_reminder, remove_reminder

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_MESSAGE, reply_markup=start_register_keyboard)


@router.callback_query(F.data == "start_register")
async def cmd_start_register(callback: CallbackQuery, state: FSMContext):
    user = get_user(Session(), user_id=callback.from_user.id)
    if user:
        await callback.message.answer("У вас уже есть активный аккаунт! ✅")
        return
    await callback.message.answer(REGISTER_MESSAGE)
    await state.set_state(RegisterStates.username)


@router.message(RegisterStates.username)
async def process_username(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Имя пользователя должно содержать минимум 5 символов. Пожалуйста, введите другое имя.")
        return
    
    session = Session()
    existing_user = get_user_by_username(session, message.text)
    
    if existing_user:
        await message.answer("Это имя уже занято. Пожалуйста, выберите другое имя.")
        return
    
    await state.update_data(username=message.text)
    await message.answer("Выберите валюту:", reply_markup=currency_keyboard)
    await state.set_state(RegisterStates.currency)


@router.callback_query(RegisterStates.currency)
async def process_currency(callback: CallbackQuery, state: FSMContext):
    await state.update_data(currency=callback.data[-3:])
    await callback.message.answer("Выберите время напоминания:", reply_markup=reminder_keyboard)
    await state.set_state(RegisterStates.reminder_time)


@router.callback_query(RegisterStates.reminder_time)
async def process_reminder_time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(reminder_time=callback.data[-5:].replace('_', ':'))
    data = await state.get_data()
    
    session = Session()
    existing_user = get_user_by_username(session, data["username"])
    
    if existing_user:
        await callback.message.answer("Это имя уже занято. Пожалуйста, выберите другое имя.")
        await state.clear()
        await callback.message.answer(REGISTER_MESSAGE)
        await state.set_state(RegisterStates.username)
        return
    
    # Создаем пользователя
    create_user(
        session=session,
        user_id=callback.from_user.id,
        username=data["username"],
        currency=data["currency"],
        reminder_time=data["reminder_time"]
    )
    
    # Планируем напоминание
    schedule_reminder(callback.bot, callback.from_user.id, data["reminder_time"])
    
    await callback.message.answer("Регистрация завершена! ✅")
    await state.clear()


@router.callback_query(F.data.startswith("change_reminder_"))
async def change_reminder_time(callback: CallbackQuery):
    new_time = callback.data.split("_")[-1].replace('_', ':')
    session = Session()
    
    # Обновляем время в базе данных
    update_user(session, callback.from_user.id, reminder_time=new_time)
    
    # Обновляем напоминание
    schedule_reminder(callback.bot, callback.from_user.id, new_time)
    
    await callback.message.answer(f"Время напоминания изменено на {new_time}! ✅")


@router.message(Command("settings"))
async def show_settings(message: Message):
    """Показать настройки пользователя"""
    session = Session()
    user = get_user(session, message.from_user.id)
    if not user:
        await message.answer("Вы не зарегистрированы! Используйте /start для регистрации.")
        return
    
    await message.answer(
        f"⚙️ Настройки\n\n"
        f"Текущее время напоминания: {user.reminder_time}",
        reply_markup=get_settings_keyboard()
    )


@router.callback_query(F.data == "show_reminder_times")
async def show_reminder_times(callback: CallbackQuery):
    """Показать варианты времени для напоминания"""
    await callback.message.edit_text(
        "Выберите новое время для напоминания:",
        reply_markup=get_reminder_times_keyboard()
    )