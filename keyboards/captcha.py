import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TOPUP_CAPTCHA_ANSWER = "🚗"
TOPUP_CAPTCHA_POOL = ["🍎", "🚗", "🐶", "⚽️"]

WITHDRAW_CAPTCHA_ANSWER = "🥮"
WITHDRAW_CAPTCHA_POOL = ["♦️", "🥮", "🍰", "🍅", "🌩", "🫀", "🔫", "🧿", "🧀"]


def topup_captcha_kb() -> InlineKeyboardMarkup:
    options = TOPUP_CAPTCHA_POOL.copy()
    random.shuffle(options)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=e, callback_data=f"captcha:{e}") for e in options]
        ]
    )


def withdraw_captcha_kb() -> InlineKeyboardMarkup:
    options = WITHDRAW_CAPTCHA_POOL.copy()
    random.shuffle(options)
    rows = [options[i:i+3] for i in range(0, len(options), 3)]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=e, callback_data=f"captcha:{e}") for e in row]
            for row in rows
        ]
    )
