from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_register_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Зарегистрироваться", callback_data="start_register")]
    ]
)

currency_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Рубль", callback_data="currency_rub")],
        [InlineKeyboardButton(text="🇺🇸 Доллар", callback_data="currency_usd")],
        [InlineKeyboardButton(text="🇪🇺 Евро", callback_data="currency_eur")],
    ]
)

reminder_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔔 9:00", callback_data="set_reminder_09_00")],
        [InlineKeyboardButton(text="🔔 12:00", callback_data="set_reminder_12_00")],
        [InlineKeyboardButton(text="🔔 15:00", callback_data="set_reminder_15_00")],
        [InlineKeyboardButton(text="🔔 18:00", callback_data="set_reminder_18_00")],
        [InlineKeyboardButton(text="🔔 21:00", callback_data="set_reminder_21_00")],
    ]
)

def get_settings_keyboard(current_time: str = None) -> InlineKeyboardMarkup:
    """Клавиатура для настроек пользователя"""
    keyboard = [
        [InlineKeyboardButton(text="Изменить время напоминания ⏰", callback_data="show_reminder_times")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

reminder_times = ["09:00", "12:00", "15:00", "18:00", "21:00"]

def get_reminder_times_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора времени напоминания"""
    keyboard = []
    for time in reminder_times:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{time}",
                callback_data=f"change_reminder_{time}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)