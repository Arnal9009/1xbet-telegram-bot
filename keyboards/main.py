from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb(t: dict) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["btn_topup"]), KeyboardButton(text=t["btn_withdraw"])],
            [KeyboardButton(text=t["btn_rules"])],
            [KeyboardButton(text=t["btn_change_lang"]), KeyboardButton(text=t["btn_las_vegas"])],
        ],
        resize_keyboard=True,
    )


def language_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский")],
            [KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🇰🇬 Кыргызча")],
        ],
        resize_keyboard=True,
    )
